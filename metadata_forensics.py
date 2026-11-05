
from pypdf import PdfReader
from docx import Document
import os


def analyze_metadata(file):

    filename = file.filename

    extension = os.path.splitext(filename)[1].lower()

    metadata = {
        "filename": filename,
        "file_type": extension,
        "author": "Not Available",
        "created": "Not Available",
        "modified": "Not Available",
        "creator": "Not Available",
        "status": "Analysis Completed"
    }

    try:

        if extension == ".pdf":

            reader = PdfReader(file.stream)

            info = reader.metadata

            if info:

                metadata["author"] = str(
                    info.author or "Not Available"
                )

                metadata["created"] = str(
                    info.creation_date or "Not Available"
                )

                metadata["modified"] = str(
                    info.modification_date or "Not Available"
                )

                metadata["creator"] = str(
                    info.creator or "Not Available"
                )

        elif extension == ".docx":

            document = Document(file.stream)

            props = document.core_properties

            metadata["author"] = (
                props.author or "Not Available"
            )

            metadata["created"] = str(
                props.created or "Not Available"
            )

            metadata["modified"] = str(
                props.modified or "Not Available"
            )

            metadata["creator"] = (
                props.last_modified_by or "Not Available"
            )

        elif extension == ".txt":

            metadata["status"] = (
                "TXT does not contain standard document metadata"
            )

        else:

            metadata["status"] = "Unsupported file format"

    except Exception as e:

        metadata["status"] = "Error: " + str(e)

    return metadata
