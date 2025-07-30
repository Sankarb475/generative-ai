# using token as a length_function in chunking

document_text = """
# The Rise of Renewable Energy

## Introduction
Renewable energy sources are rapidly gaining prominence as the world seeks sustainable alternatives to fossil fuels. These sources, naturally replenished on a human timescale, include sol

## Solar Power
Solar power harnesses sunlight using photovoltaic (PV) panels or concentrated solar power (CSP) systems. PV technology converts sunlight directly into electricity, making it versatile for

## Wind Power
Wind power utilizes wind turbines to convert wind energy into electricity. Modern wind turbines are highly efficient and can be deployed both onshore and offshore. Offshore wind farms, in

## Hydropower
Hydropower generates electricity by harnessing the energy of flowing water, typically through dams or run-of-river systems. It is one of the oldest and most established forms of renewable

## Geothermal Energy
Geothermal energy taps into the Earth's internal heat. Geothermal power plants use steam from reservoirs deep within the Earth to drive turbines and generate electricity. This source offe

## Biomass Energy
Biomass energy is derived from organic matter, such as agricultural waste, forest residues, and dedicated energy crops. It can be converted into electricity, heat, or liquid fuels (biofue

## Conclusion
The diverse portfolio of renewable energy technologies offers a promising path towards a sustainable energy future. Continued investment in research, development, and infrastructure is es
"""



from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer

# token using hugging face OLLAMA open source 
llama_tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

def llama_token_len(text):
    return len(llama_tokenizer.encode(text))

# Customizing separators for a Markdown-like document
# We want to prioritize splitting by headings, then paragraphs, then lines, then characters.
markdown_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
    length_function=llama_token_len,
    separators=["\n## ", "\n##", "\n\n", "\n", " ", ""], # Order matters!
    is_separator_regex=False,
)

markdown_chunks = markdown_splitter.split_text(document_text)

print(f"Original document length (Llama 2 tokens): {llama_token_len(document_text)} tokens\n")
print(f"--- Markdown-aware Chunking (Chunk Size: 50, Overlap: 10) ---")
print(f"Number of chunks: {len(markdown_chunks)}\n")

for i, chunk in enumerate(markdown_chunks):
    print(f"--- Chunk {i+1} (Length: {len(chunk)} characters) ---")
    print(chunk)
    print("\n" + "="*50 + "\n")
