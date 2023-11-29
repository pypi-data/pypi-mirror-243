from jinja2 import Template
from jinja2 import DebugUndefined
import shutil
import os
from logs.manager import LoggingManager

class TemplateManager(object):
    def __init__(self, context={}):
        self._context = context

    @property
    def context(self):
        """Getter method for context."""
        return self._context

    @context.setter
    def context(self, value):
        """Setter method for context."""
        self._context = value

    def __read_template_file(self, path):
        with open(path, "r") as template_file:
            self.content = template_file.read()

    def __create_template(self):
        self.template = Template(self.content, undefined=DebugUndefined)

    def render_template_from_file(self, path):
        self.__read_template_file(path)
        self.__create_template()
        return self.template.render(self.context)

    def render_template(self, content):
        try:
            self.content = content
            self.__create_template()
            return self.template.render(self.context)
        except Exception as e:
            LoggingManager.display_single_message(
                f"Unexpected {type(e)=}: {e=}"
            )
            return content
    
    def copytree(self, source_directory, target_directory):
        for obj in os.listdir(source_directory):
            obj_path = os.path.join(source_directory, obj)
            if os.path.isdir(obj_path):
                self.copytree(
                    obj_path, os.path.join(target_directory, obj)
                )
            else:
                self.copy(obj_path, target_directory)

        # return shutil.copytree(
        #     source_directory,
        #     target_directory,
        #     dirs_exist_ok=True,
        # )
    
    def copy(self, source_file_path, target_directory):

        # Get the target directory created recursively!
        os.makedirs(target_directory, exist_ok=True)
        source_file_content = None
        
        file_name = os.path.basename(source_file_path)
        output_file_path = os.path.join(target_directory, file_name)

        try:
            # Try to read the file as text and write it to the output file
            with open(source_file_path, "r") as source_file_stream:
                source_file_content = source_file_stream.read()
            
            with open(output_file_path, "w") as output_file:
                output_file.write(self.render_template(source_file_content))
        except UnicodeDecodeError:
            shutil.copy(source_file_path, target_directory)

        return output_file_path
