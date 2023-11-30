# th€ main function for all services testing
from ..folderforge.core import FolderForge


def main():
	FolderForge("config.json").forge()
		
if __name__ == "__main__":
	main()