import time
from pathlib import Path

import click


class TypeWriter:
	def __init__(self, path: Path) -> None:
		self.path = path

	def __call__(self, data: str) -> None:
		with self.path.open("a") as f:  # Open file in append mode
			f.write(data)

def typewriter(text:str, destination: Path) -> None:
	if not destination.exists():
		destination.touch()
	time.sleep(5)
	for char in text:
		TypeWriter(destination)(char)
		time.sleep(0.1)


def parse_and_write(markdown_path: Path) -> None:
	content = markdown_path.read_text()
	sections = content.split("---")
	file_name = ""
	for section in sections[1:]:  # Skip the first empty section
		lines = section.strip().split("\n")
		if len(lines) < 2:
			file_name = lines[0].strip()
			continue
		file_content = "\n".join(lines)
		typewriter(file_content, Path(file_name))

@click.command()
@click.argument("markdown_path", type=click.Path(exists=True),default="README.md")
def main(markdown_path: str) -> None:
	parse_and_write(Path(markdown_path))

if __name__ == "__main__":
	main() # pylint: disable=no-value-for-parameter