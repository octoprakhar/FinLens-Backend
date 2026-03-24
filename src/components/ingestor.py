import os
import re
import json

from src.entity.config import IngestConfig
from src.entity.artifacts import IngestArtifact
import fitz

class IngestPdf:
    def __init__(self, config:IngestConfig):
        self.output_dir = config.md_file_path_dir
        self.chunk_dir = config.chunk_file_path_dir
        self.config = config
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.chunk_dir, exist_ok=True)

    def _clean_text(self,text:str)->str:
        lines = text.split("\n")
    
        paragraphs = []
        current_para = []

        for line in lines:
            line = line.strip()

            if not line:
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                continue

            current_para.append(line)

        if current_para:
            paragraphs.append(" ".join(current_para))

        return "\n\n".join(paragraphs)
    
    ## Chunking helper functions 
    def _split_pages(self,md_text: str):
        pages_raw = md_text.split("# Page")
        pages = []

        for p in pages_raw:
            p = p.strip()
            if not p:
                continue

            parts = p.split("\n", 1)
            if len(parts) == 2:
                page_text = parts[1]
            else:
                page_text = parts[0]

            pages.append(page_text.strip())

        return pages
    
    def _split_paragraphs(self,text: str):
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        # Remove junk paragraphs
        cleaned_paragraphs = []
        for p in paragraphs:
            if p == "---":
                continue
            if len(p) < 10:  # very small noise
                continue
            cleaned_paragraphs.append(p)

        return cleaned_paragraphs
    
    def _split_sentences(self,text: str):
        return re.split(r'(?<=[.!?])\s+', text)
    
    def _create_chunks(self,text: str, page_num: int, max_words: int = 120):
        sentences = self._split_sentences(text)

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            words = sentence.split()
            word_count = len(words)

            if current_length + word_count > max_words:
                if current_chunk:
                    chunks.append({
                        "text": " ".join(current_chunk),
                        "page": page_num
                    })
                current_chunk = []
                current_length = 0

            current_chunk.append(sentence)
            current_length += word_count

        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "page": page_num
            })

        return chunks




    def _pdf_to_md_converter(self, file_source, md_file_path):
        md_output = ""
        # If file_source is a string (local path), open it normally.
        # If file_source is a 'file-like object' (from FastAPI), read it as bytes.
        if isinstance(file_source, str):
            doc = fitz.open(file_source)
        else:
            # file_source.read() gets the bytes from the internet upload
            pdf_bytes = file_source.file.read() 
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_num, page in enumerate(doc):
            raw_text = page.get_text()
            cleaned_text = self._clean_text(raw_text)

            md_output += f"# Page {page_num + 1}\n\n{cleaned_text}\n\n---\n\n"

        with open(md_file_path,"w",encoding="utf-8") as f:
            f.write(md_output)

        return md_file_path
    

                

    def _process_chunks(self, md_file_path, chunk_file_path):
        with open(md_file_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        pages = self._split_pages(md_text)
        all_chunks = []

        for page_num, page_text in enumerate(pages, start=1):
            paragraphs = self._split_paragraphs(page_text)

            for para in paragraphs:
                chunks = self._create_chunks(para, page_num, self.config.max_word_in_chunk)
                all_chunks.extend(chunks)
        
        with open(chunk_file_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)

        return chunk_file_path

    def ingestData(self, file_source)->IngestArtifact:
        md_file_path = os.path.join(self.config.md_file_path_dir, self.config.md_file_name)
        chunk_file_path = os.path.join(self.config.chunk_file_path_dir, self.config.chunk_file_name)
        
        md_file = self._pdf_to_md_converter(file_source,md_file_path=md_file_path)
        chunk_file = self._process_chunks(md_file_path=md_file_path, chunk_file_path=chunk_file_path)

        return IngestArtifact(md_file_path=md_file,chunk_file_path=chunk_file)