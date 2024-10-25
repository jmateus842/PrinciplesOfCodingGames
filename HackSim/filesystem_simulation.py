import os
import json
import random

class FileSystemSimulation:
    def __init__(self):
        self.root = Directory('/')
        self.current_directory = self.root
        self.load_config()
        self._create_file_structure()

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            # Configuracion predeterminada si no se encuentra el archivo de configuracion
            self.config = {
                "game": {
                    "target_file": "install.txt",
                    "target_content": "MALWARE!!!",
                    "file_structure": {}  # Estructura vacia para ser completada en _create_file_structure
                }
            }
            print("Archivo de configuracion no encontrado. Utilizando configuracion predeterminada.")

    def _create_file_structure(self):
        # Utilizar estructura predeterminada si no hay configuracion definida
        if not self.config['game']['file_structure']:
            self._create_default_file_structure()
        else:
            self._create_structure_from_config(self.root, self.config['game']['file_structure'])

    def _create_default_file_structure(self):
        # Inicializacion de la estructura de archivos base
        home = self.root.add_directory('home')
        user = home.add_directory('user')
        user.add_file('readme.txt', 'Welcome to the system!')
        
        # Directorio de documentos
        documents = user.add_directory('documents')
        documents.add_file('notes.txt', 'Check all directories carefully.')
        documents.add_file('todo.txt', '1. Finish project report\n2. Call mom\n3. Buy groceries')
        documents.add_file('homework.txt', 'Just some regular homework. Nothing suspicious here!')
        
        # Directorio de descargas
        downloads = user.add_directory('downloads')
        downloads.add_file('funny_cat.jpg', '[Image data]')
        downloads.add_file('invoice_2023.pdf', '[PDF data]')
        
        # Directorio del juego
        new_game = downloads.add_directory('new_game')
        new_game.add_file('install.txt', 'You\'re about to be hacked. I AM MALWARE.')
        
        # Directorio de proyectos
        projects = user.add_directory('projects')
        projects.add_file('system_update.log', '2023-04-15 11:45:30 INFO: System update completed successfully')
        projects.add_file('project_outline.txt', 'Project goals:\n1. Implement new features\n2. Fix known bugs\n3. Improve performance')
        
        # Directorio oculto
        hidden = user.add_directory('.hidden')
        hidden.add_file('secret.txt', 'You\'re about to be NOT hacked. GOOD LUCK THOUGH.')
        
        # Directorios del sistema
        tmp = self.root.add_directory('tmp')
        tmp.add_file('temp.txt', 'This is a temporary file.')
        
        var = self.root.add_directory('var')
        log = var.add_directory('log')
        log.add_file('system.log', '2023-04-15 10:30:22 INFO: System startup\n2023-04-15 10:30:25 WARNING: Disk space low')

    def _create_structure_from_config(self, parent, structure):
        for name, content in structure.items():
            if isinstance(content, dict):
                new_dir = parent.add_directory(name)
                self._create_structure_from_config(new_dir, content)
            else:
                parent.add_file(name, content)

    def execute_command(self, command, args):
        if command == 'ls':
            return self._ls(args)
        elif command == 'cd':
            return self._cd(args)
        elif command == 'pwd':
            return self._pwd()
        elif command == 'cat':
            return self._cat(args)
        elif command == 'mkdir':
            return self._mkdir(args)
        elif command == 'rm':
            return self._rm(args)
        elif command == 'touch':
            return self._touch(args)
        elif command == 'echo':
            return self._echo(args)
        else:
            return f"Command not found: {command}"

    def _ls(self, args):
        target_dir = self.current_directory
        if args:
            target_dir = self._get_directory(args[0])
            if not target_dir:
                return f"ls: cannot access '{args[0]}': No such file or directory"
        
        items = list(target_dir.subdirectories.keys()) + list(target_dir.files.keys())
        return ' '.join(items)

    def _cd(self, args):
        if not args:
            self.current_directory = self.root
            return ""
        
        path = args[0]
        if path == '..':
            if self.current_directory.parent:
                self.current_directory = self.current_directory.parent
        elif path == '/':
            self.current_directory = self.root
        else:
            new_dir = self._get_directory(path)
            if new_dir:
                self.current_directory = new_dir
            else:
                return f"cd: {path}: No such file or directory"
        return ""

    def _pwd(self):
        path = []
        current = self.current_directory
        while current:
            path.append(current.name)
            current = current.parent
        return '/' + '/'.join(reversed(path[:-1]))

    def _cat(self, args):
        if not args:
            return "cat: missing operand"
        
        file_name = args[0]
        if file_name in self.current_directory.files:
            return self.current_directory.files[file_name]
        else:
            return f"cat: {file_name}: No such file or directory"

    def _mkdir(self, args):
        if not args:
            return "mkdir: missing operand"
        
        dir_name = args[0]
        if dir_name in self.current_directory.subdirectories:
            return f"mkdir: cannot create directory '{dir_name}': File exists"
        
        self.current_directory.add_directory(dir_name)
        return ""

    def _rm(self, args):
        if not args:
            return "rm: missing operand"
        
        name = args[0]
        if name in self.current_directory.files:
            del self.current_directory.files[name]
        elif name in self.current_directory.subdirectories:
            del self.current_directory.subdirectories[name]
        else:
            return f"rm: cannot remove '{name}': No such file or directory"
        return ""

    def _touch(self, args):
        if not args:
            return "touch: missing file operand"
        
        file_name = args[0]
        if file_name not in self.current_directory.files:
            self.current_directory.add_file(file_name, '')
        return ""

    def _echo(self, args):
        return ' '.join(args)

    def _get_directory(self, path):
        if path.startswith('/'):
            current = self.root
            path = path[1:]
        else:
            current = self.current_directory
        
        for part in path.split('/'):
            if part == '':
                continue
            elif part == '..':
                if current.parent:
                    current = current.parent
            elif part in current.subdirectories:
                current = current.subdirectories[part]
            else:
                return None
        return current

class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subdirectories = {}
        self.files = {}

    def add_directory(self, name):
        new_dir = Directory(name, self)
        self.subdirectories[name] = new_dir
        return new_dir

    def add_file(self, name, content):
        self.files[name] = content

class File:
    def __init__(self, name, content):
        self.name = name
        self.content = content
