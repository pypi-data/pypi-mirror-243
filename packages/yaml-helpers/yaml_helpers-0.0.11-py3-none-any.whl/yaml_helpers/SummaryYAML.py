import os
from pathlib import Path
from threading import Lock

import yaml

from .EmbeddingYAML import EmbeddingYAML
from .utils import manage_code_length
# from .config import PROJECT_ROOT


REQUIRED_ENTITY_FIELDS = ["name", "description", "functional_category", "dependencies", "nested"]
REQUIRED_FILE_FIELDS = ["name", "description", "entities"]

class SummaryYAML:
    def __init__(self, root_directory, embedding_mode=False):
        self.root_directory = Path(root_directory)
        self.current_directory = self.root_directory
        self.current_file = None
        self.current_entity = None
        self.current_entity_ancestry = []
        self.summary_data = self.load_yaml_recursive(self.root_directory)
        self.yaml_lock = Lock()

        if embedding_mode:
            embedding_file = os.path.join(self.root_directory, '.embeddings.yaml')
            self.embedding_yaml = EmbeddingYAML(embedding_file)
        else:
            self.embedding_yaml = None

    def load_yaml_recursive(self, directory):
        yaml_path = os.path.join(directory, '.summary.yaml')
        if not os.path.exists(yaml_path):
            return {}

        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        subdirectories = data.get('subdirectories', [])
        data['subdirectories'] = {}
        for subdirectory in subdirectories:
            subdirectory_path = os.path.join(directory, subdirectory)
            data['subdirectories'][subdirectory] = self.load_yaml_recursive(subdirectory_path)

        return data

    def set_current_directory(self, new_directory):
        # Check if the new_directory is a direct subdirectory of the current_directory
        potential_new_directory = self.current_directory / new_directory

        if potential_new_directory.exists() and potential_new_directory.is_dir():
            self.current_directory = Path(potential_new_directory)
            return

        # Check if new_directory is a subdirectory of root_directory
        new_directory_path = Path(new_directory)

        try:
            new_directory_path.relative_to(self.root_directory)
        except ValueError:
            print("The new directory must be a subdirectory of the root directory or a direct subdirectory of the current directory.")
            print(f"This is the directory we tried to enter: {new_directory}")
            return

        self.current_directory = new_directory_path

    def set_current_file(self, file_name, directory=None):
        if directory:
            self.set_current_directory(directory)
        data = self._navigate_to_current_directory()
        potential_files = [f for f in data.get('files', []) if f['name'] == file_name]
        if len(potential_files) == 0:
            self.current_file = None
        else:
            self.current_file = potential_files[0]

    def set_bookmark(self, bookmark, reset=False):
        if reset:
            self.reset_bookmark()
        if bookmark[0].get('directory'):
            self.set_current_directory(bookmark[0].get('directory'))
            self.set_current_file(bookmark[0].get('file'))
            if len(bookmark) > 1:
                bookmark = bookmark[1:]
                self.set_current_entity(bookmark)
            else:
                self.current_entity = None
        else:
            self.set_current_entity(bookmark)

    def set_current_entity(self, entity_info, start_line=None, file_name=None, directory=None):
        if file_name:
            self.set_current_file(file_name, directory)
        if not self.current_file:
            raise ValueError("Current file is not set.")
        if isinstance(entity_info, str):
            # Handle non-nested entities
            self.current_entity = self.find_entity(self.current_file, entity_info, start_line)
            self.current_entity_ancestry = [self.current_entity]
        elif isinstance(entity_info, list):
            self.current_entity_ancestry = []
            # Handle nested entities
            parent = self.current_file
            for info in entity_info:
                entity = self.find_entity(parent, info['name'], info.get('start_line'))
                if entity is None:
                    raise ValueError(f"Entity {info['name']} not found.")
                self.current_entity_ancestry.append(entity)
                parent = entity
            self.current_entity = entity

        if self.current_entity is None:
            raise ValueError(f"Entity not found.")

    def reset_bookmark(self):
        self.current_directory = self.root_directory
        self.current_file = None
        self.current_entity = None
        self.current_entity_ancestry = []

    def get_current_bookmark(self):
        if not self.get_current_file(name_only=True):
            return [{'directory': self.get_current_directory(str_only=True)}]
        base_list = [{'directory': self.get_current_directory(str_only=True), 'file': self.get_current_file(name_only=True)}]
        base_list.extend([{'name': e['name'], 'start_line': e['start_line']} for e in self.current_entity_ancestry])
        return base_list

    def find_entity(self, parent, entity_name, start_line=None):
        if parent is self.current_file:
            candidates = [e for e in parent.get('entities', []) if e['name'] == entity_name]
        else:
            candidates = [e for e in parent.get('nested', []) if e['name'] == entity_name]

        if start_line:
            top_candidates = [e for e in candidates if e['start_line'] == start_line]
            if len(top_candidates) == 0:
                return None
            return top_candidates[0]
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            raise ValueError(f"Multiple entities with the name '{entity_name}' found. Please specify a start line.")
        return None

    def get_files_in_current_directory(self):
        data = self._navigate_to_current_directory()
        return [f['name'] for f in data.get('files', [])]

    def get_subdirectories_in_current_directory(self):
        data = self._navigate_to_current_directory()
        return [d for d in data.get('subdirectories', [])]

    def get_entities_in_current_file(self):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        return [[{'name': e['name'], 'start_line': e['start_line']}] for e in self.current_file.get('entities', [])]

    def get_current_file(self, name_only=False):
        if self.current_file:
            if name_only:
                return self.current_file['name']
            return os.path.join(self.current_directory, self.current_file['name'])
        return None

    def get_current_directory(self, str_only=False):
        if str_only:
            return str(self.current_directory)
        return self.current_directory

    def get_current_entity(self):
        return self.current_entity

    def get_nested_entities(self, include_start_line=False):
        if self.current_entity is None:
            return None

        nested_entities = self.current_entity.get('nested', [])

        if include_start_line:
            return [{'name': e['name'], 'start_line': e['start_line']} for e in nested_entities]
        else:
            return [e['name'] for e in nested_entities]

    def add_field(self, field_name, value):
        with self.yaml_lock:
            if not self.current_entity:
                raise ValueError("Current entity is not set.")
            self.current_entity[field_name] = value

    def add_field_to_current_file(self, field_name, value):
        with self.yaml_lock:
            if not self.current_file:
                raise ValueError("Current file is not set.")
            self.current_file[field_name] = value

    def add_field_to_current_directory(self, field_name, value):
        with self.yaml_lock:
            data = self._navigate_to_current_directory()
            data[field_name] = value

    def get_embedding_for_current_entity(self):
        if not self.embedding_yaml:
            raise ValueError("Embedding mode is off.")
        if not self.current_entity:
            raise ValueError("Current entity is not set.")
        return self.embedding_yaml.get_embedding_by_id(self.current_entity['entity_id'])

    def save(self):
        # Build the path to the correct .summary.yaml based on the current directory
        save_path = os.path.join(self.current_directory, '.summary.yaml')

        # Navigate the summary_data dictionary to the data corresponding to the current directory
        data_to_save = self._navigate_to_current_directory().copy()

        data_to_save['subdirectories'] = [dir_name for dir_name in data_to_save.get('subdirectories',[])]

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(data_to_save, f)

    def get_current_file_type(self):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        return self.current_file.get('file_type', None)

    def read_code_lines(self, start_line=None, end_line=None):
        file_path = os.path.join(self.current_directory, self.current_file['name'])
        if start_line == None:
            start_line = 0
        if end_line != None:
            end_line += 1
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return ''.join(lines[start_line:end_line]).rstrip()  # Assuming 1-based line numbers in YAML

    def get_source_file_path(self):
        return os.path.join(self.current_directory, self.current_file['name'])

    def get_imports_in_current_file(self, up_to_line=None):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        imports = self.current_file.get('imports', [])
        if up_to_line:
            imports = [imp for imp in imports if imp['end_line'] <= up_to_line]
        code_imports = [{'info': imp, 'code': self.read_code_lines(imp['start_line'], imp['end_line'])} for imp in
                        imports]
        return code_imports

    def get_declarations_in_current_file(self, up_to_line=None):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        declarations = self.current_file.get('declarations', [])
        if up_to_line:
            declarations = [dec for dec in declarations if dec['end_line'] <= up_to_line]
        code_declarations = [{'info': dec, 'code': self.read_code_lines(dec['start_line'], dec['end_line'])} for dec in
                             declarations]
        return code_declarations

    def get_imports_and_declarations_in_current_file(self, up_to_line=True):
        if self.get_current_entity() and up_to_line:
            imports_and_declarations = self.get_declarations_in_current_file(up_to_line=self.get_current_entity()['start_line']) + self.get_imports_in_current_file(up_to_line=self.get_current_entity()['start_line'])
        else:
            imports_and_declarations = self.get_declarations_in_current_file() + self.get_imports_in_current_file()
        imports_and_declarations = sorted(imports_and_declarations, key=lambda x: x['info']['start_line'])
        imports_and_declarations_code = '\n'.join(item['code'] for item in imports_and_declarations)

        return imports_and_declarations_code

    def get_entity_code(self, reduced=True):
        if not self.current_file or not self.current_entity:
            raise ValueError("Either current file or entity is not set.")

        start_line = self.current_entity['start_line']
        end_line = self.current_entity['end_line']

        file_path = os.path.join(self.current_directory, self.current_file['name'])

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        nested_entities = self.current_entity.get('nested', [])
        nested_entities = sorted(nested_entities, key=lambda x: x['start_line'])

        entity_code = ''
        last_line = start_line  # Initialize last_line to start_line

        if reduced:
            for nested_entity in nested_entities:
                nested_start = nested_entity['start_line']
                nested_end = nested_entity['end_line']
                nested_declaration_end = nested_entity.get('declaration_end_line', nested_start)
                description = nested_entity.get('description', '')

                # Get the indentation level from the nested entity's first line
                indentation = ''
                if nested_start < len(lines):
                    indentation = lines[nested_start][:len(lines[nested_start]) - len(lines[nested_start].lstrip())]

                # Add lines before the nested entity
                entity_code += ''.join(lines[last_line:nested_start])
                # Add the nested entity's function definition line
                entity_code += ''.join(lines[nested_start:nested_declaration_end + 1])
                # Add the description as a comment, replacing the function body
                entity_code += f"{indentation}    # {description}\n"

                last_line = nested_end + 1  # Update last_line to after the nested entity

        # Add remaining lines after the last nested entity
        actual_code = manage_code_length(''.join(lines[last_line:end_line + 1]).rstrip(), self.get_current_file_type())
        entity_code += actual_code

        return entity_code

    def get_current_file_info(self):
        return self.current_directory, self.current_file['name'] if self.current_file else None

    def _get_entity_info(self, entity_info, level=0, prefix='  '):
        entity_info_str = ''

        # Set the current entity to this entity
        self.set_bookmark(entity_info)

        # Get its details
        entity = self.get_current_entity()

        # Create the string for this entity
        entity_info_str += f"{prefix * level}{entity['name']}: {entity.get('description', 'No description')}\n"

        # Check for nested entities within this entity
        nested_entities = self.get_nested_entities(include_start_line=True)

        # Recursively get info for each nested entity
        for nested_entity in nested_entities:
            self.set_bookmark(entity_info)
            current_entity_bookmark = self.get_current_bookmark()
            nested_entity_info = current_entity_bookmark + [nested_entity]
            entity_info_str += self._get_entity_info(nested_entity_info, level + 1)

        return entity_info_str

    def get_all_entities_info_in_current_file(self):
        all_entities_info = ""

        # First, get the list of top-level entities in the current file
        entities_in_file = self.get_entities_in_current_file()

        # Loop through each top-level entity to get its info and its nested entities info
        for entity_info in entities_in_file:
            all_entities_info += self._get_entity_info(entity_info)

        return all_entities_info

    def get_all_file_info_in_current_directory(self):
        files_info_str = ''
        files = self.get_files_in_current_directory()
        bookmark = self.get_current_bookmark()
        for file in files:
            self.set_current_file(file)
            files_info_str += f"{file}: {self.current_file.get('description', 'No description')}\n"
        self.set_bookmark(bookmark)
        return files_info_str

    def get_all_subdirectory_info_in_current_directory(self):
        subdirectory_info_str = ''
        subdirectories = self.get_subdirectories_in_current_directory()
        bookmark = self.get_current_bookmark()
        for subdirectory in subdirectories:
            self.set_current_directory(subdirectory)
            data = self._navigate_to_current_directory()
            subdirectory_info_str += f"{self.current_directory.name}: {data.get('directory_description', 'No description')}\n"
            self.set_bookmark(bookmark)
        return subdirectory_info_str

    def _navigate_to_current_directory(self):
        data = self.summary_data

        relative_path = self.current_directory.relative_to(self.root_directory)

        # Loop through each part of the relative path
        for parent in reversed(Path(relative_path).parents):
            sub_dir = parent.name
            if sub_dir:
                data = data['subdirectories'].get(sub_dir, {})

        # Finally, navigate to the base of the relative path (if it exists)
        base = Path(relative_path).name
        if base:
            data = data['subdirectories'].get(base, {})

        return data

    def get_directory_summary(self, summary_data=None):
        if not summary_data:
            summary_data = self.summary_data
        summary_data_new = {'directory_description': summary_data['directory_description'], "files": [], 'subdirectories': {}}
        for file in summary_data['files']:
            new_file = {}
            new_file['name'] = file["name"]
            new_file['entities'] = self.get_entities(file["entities"])
            summary_data_new["files"].append(new_file)
        subdirectories_new = {subdir_name: self.get_directory_summary(subdir_data) for subdir_name, subdir_data
                              in summary_data['subdirectories'].items()}
        summary_data_new['subdirectories'] = subdirectories_new
        print(f"directory_summary: {summary_data_new}")
        return summary_data_new

    def get_entities(self, entities):
        new_entities = []
        for entity in entities:
            if entity["nested"]:
                self.get_entities(entity["nested"])
            new_entities.append({key: value for key, value in entity.items() if key in REQUIRED_ENTITY_FIELDS})
        return new_entities

    def get_code_from_path(self, code_lines=None, show_nested=True):
        entities_code = ""
        if code_lines:
            imports_and_declarations_code = self.get_imports_and_declarations_in_current_file()
            if len(code_lines) > 1:
                entities_lines = [[{"name": entity["name"], "start_line": entity["start_line"]}]
                                  for entity in self.current_file["entities"]
                                  if (entity["start_line"] < code_lines[0] <= entity["end_line"])
                                  or (code_lines[0] < entity["start_line"] <= code_lines[1])
                                  or (entity["start_line"] == code_lines[0])
                                  or (entity["start_line"] == code_lines[1])]
            else:
                entities_lines = [[{"name": entity["name"], "start_line": entity["start_line"]}]
                                  for entity in self.current_file["entities"]
                                  if (entity["start_line"] <= code_lines[0] <= entity["end_line"])]
            for entity_info in entities_lines:
                self.set_bookmark(entity_info)
                entities_code += self.get_entity_code(reduced=not show_nested) + "\n"
            final_code = "# For context: Imports and declarations from the file\n"
            final_code += f"{imports_and_declarations_code}\n"
            final_code += "# Start: Code snippet of interest\n"
            final_code += entities_code
            final_code += "\n# End: Code snippet of interest\n"
        else:
            final_code = self.read_code_lines()
            entities_code = final_code
        return final_code, entities_code

    def get_function_names_from_path(self, code_lines=None, show_nested=True):
        if code_lines:
            if len(code_lines) > 1:
                file_entities = [{"name": entity["name"], "nested": entity["nested"]}
                                  for entity in self.current_file["entities"]
                                  if (entity["start_line"] < code_lines[0] <= entity["end_line"])
                                  or (code_lines[0] < entity["start_line"] <= code_lines[1])
                                  or (entity["start_line"] == code_lines[0])
                                  or (entity["start_line"] == code_lines[1])]
            else:
                file_entities = [{"name": entity["name"], "nested": entity["nested"]}
                                  for entity in self.current_file["entities"]
                                  if (entity["start_line"] <= code_lines[0] <= entity["end_line"])]

            entities = self._get_entities_names(file_entities, show_nested)
        else:
            entities = [e[0]['name'] for e in self.get_entities_in_current_file()]
        return entities

    def _get_entities_names(self, file_entities, show_nested):
        entities = []
        for e in file_entities:
            entities.append(e["name"])
            if show_nested and e['nested']:
                self._get_entities_names(e['nested'])
        return entities

    def __getstate__(self):
        # Copy the object's dictionary
        state = self.__dict__.copy()
        # Remove the yaml_lock attribute, and any other non-serializable attributes
        del state['yaml_lock']
        return state

    def __setstate__(self, state):
        # Re-create the yaml_lock attribute, and any other non-serializable attributes
        self.yaml_lock = Lock()
        # Set all other attributes
        for key, value in state.items():
            setattr(self, key, value)


# Example usage
if __name__ == "__main__":
    path_parts = '/Users/darias/PycharmProjects/test_project/main3.py'.split("/")
    directory = "/".join(path_parts[:-1])
    file = path_parts[-1]
    summary_yaml = SummaryYAML(directory)
    summary_yaml.set_bookmark([{"directory": Path(directory), "file": file}])
    data = summary_yaml.get_function_names_from_path([11,27])

    # summary_yaml = SummaryYAML(r'/Users/darias/PycharmProjects/test_project')
    # data = summary_yaml.get_directory_summary()
    print(data)

    # summary_yaml = SummaryYAML(r'C:\Users\tamuz\codingAgents\directory_parser\coding_languages\tests')
    # new_path = r"C:\Users\tamuz\Documents\Sample_Projects\pycalc-master"
    # # new_path = r"C:\Users\tamuz\Documents\Commit_Projects\rodradar-app"
    # summary_yaml = SummaryYAML(new_path)
    # summary_yaml.get_subdirectories_in_current_directory()
    # summary_yaml.set_current_file(summary_yaml.get_files_in_current_directory()[3])
    # info_str = summary_yaml.get_all_entities_info_in_current_file()
    # print(info_str)
    # summary_yaml.set_current_entity('MyClass')
    # summary_yaml.get_nested_entities()
    # nested_path = [
    #     {'name': 'MyClass', 'start_line': 27},
    #     {'name': 'NestedClass', 'start_line': 46}
    # ]
    # summary_yaml.set_current_entity(nested_path)
    # summary_yaml = SummaryYAML(PROJECT_ROOT / 'tests', embedding_mode=True)
    # summary_yaml.set_current_file('some/sub/directory', 'example_file.py')
    # summary_yaml.set_current_entity('some_function')
    # summary_yaml.add_field('new_field', 'new_value')
    # embedding = summary_yaml.get_embedding_for_entity('some_function')
    # summary_yaml.save()
