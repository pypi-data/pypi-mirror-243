from .services import FolderForgeService, FileService, ChangeDirectoryContext

class FolderForge:
	def __init__(self, description_file_path: str):
		self.description_file_path = description_file_path
		description = FolderForgeService.readJSON(description_file_path)
		self.path = description.get("path", "")
		self.tree = description.get("tree", [])
		
		
	
	def forge(self):

		# Create the root directory, it can be empty, a simple name or a path
		FileService.createDirectory(self.path)

		with ChangeDirectoryContext(self.path):	
			for node in FolderForgeService.searchPaths(self.tree):
				type = node["type"]
				path = node["path"]
				
				if type == "file":
					FileService.createFile(path)
				elif type == "directory":
					FileService.createDirectory(path)
				else:
					raise Exception("Unknown node type: " + type)
			
			return self