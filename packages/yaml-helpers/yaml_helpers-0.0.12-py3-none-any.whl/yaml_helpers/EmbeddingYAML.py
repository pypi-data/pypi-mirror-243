import yaml

class EmbeddingYAML:
    def __init__(self, embedding_file):
        self.embedding_file = embedding_file
        self.embedding_data = self.load_yaml(embedding_file)

    def load_yaml(self, file_path):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)

    def get_embedding_by_id(self, entity_id):
        return self.embedding_data.get(entity_id, None)

    def save(self):
        with open(self.embedding_file, 'w') as f:
            yaml.dump(self.embedding_data, f)

