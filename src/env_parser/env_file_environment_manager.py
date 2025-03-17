from src.environment.environment import Environment, EnvironmentVariable
from src.utils.file_utils import write_string_to_file, read_file_to_string
from src.configs.configs import is_case_sensitive, path_to_environment_data
from src.utils.condition_utils import none_are_null

def generate_path_to_env(env_name):
    if not is_case_sensitive:
        env_name = env_name.lower()
    file_path = f'{path_to_environment_data}/{env_name}.env'
    return file_path

class EnvFileEnvironmentManager:
     
    def create_env_file_from_environment(self, path_to_env_file : str, env : Environment) -> str:
        env_str = self.create_env_str_from_environment(env)
        write_string_to_file(
            file_path=path_to_env_file,
            content=env_str,
        )
    
    
    def create_env_str_from_environment(self, env : Environment) -> str:
        env_list = [
            (
                # Write all 3 (key, value, comment) if none are null
                f'{var._key}="{var._value}"#{var._comment}' if none_are_null(var._key, var._value, var._comment,) \
                # One is null
                # if key and value are not null, only comment is null. write key value
                else f'{var._key}="{var._value}"' if none_are_null(var._key, var._value) \
                # either key or value or both are null.
                # if comment is not null, write comment
                else f'#{var._comment}"' if none_are_null(var._comment) \
                # all is null, blank line
                else ""
            )
            for var in env._variables
        ]
        env_str = '\n'.join(env_list)
        return env_str

    def parse_environment_from_env_file(self, env_name : str, path_to_env_file : str) -> Environment:
        env_str = read_file_to_string(path_to_env_file)
        return self.parse_environment_from_env_str(env_name, env_str)

    def parse_env_line(self, line: str):
        """
        CHATGPT
        Parses a line from a .env file into key, value, and comment.
        
        :param line: A single line from a .env file.
        :return: A tuple (key, value, comment) where each can be None if missing.
        """
        line = line.strip()
        
        if not line or line.startswith("#"):
            return None, None, line if line else None
        
        # old regex r'([^#=]+)?(?:\s*=\s*([^#]*))?(?:\s*#(.*))?'
        match = re.match(r'([^#=]+)?(?:\s*=\s*(["\']?.*?["\']?))?(?:\s+#(.*))?', line)
        
        if match:
            key = match.group(1).strip() if match.group(1) else None
            value = match.group(2).strip() if match.group(2) else None
            comment = match.group(3).strip() if match.group(3) else None
            return key, value, comment
        
        return None, None, None  # Fallback case
    
    def parse_environment_from_env_str(self, env_name : str, env_str : str) -> Environment:
        lines = env_str.split('\n')
        environment = Environment(name=env_name)
        for line in lines:
            key, value, comment = self.parse_env_line(line)
            if (value is not None) and ((value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))):
                # Removes quotes from string entries
                value = value[1:-1]
            environment.add_variable(
                EnvironmentVariable(
                    key = key,
                    value = value,
                    comment = comment,
                )
            )
        
        return environment


