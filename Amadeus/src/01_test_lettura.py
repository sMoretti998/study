import os
from langchain_community.document_loaders import PyPDFLoader

# Questo comando trova il percorso esatto della cartella 'data' 
# indipendentemente da dove lanci il terminale
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

print(f"DEBUG: Sto cercando i file in: {data_dir}")

if not os.path.exists(data_dir):
    print(f"❌ La cartella '{data_dir}' non esiste proprio!")
else:
    files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    if not files:
        print(f"❌ La cartella è stata trovata, ma è VUOTA. Metti un PDF in: {data_dir}")
    else:
        pdf_path = os.path.join(data_dir, files[0])
        print(f"📖 Amadeus sta leggendo: {pdf_path}...")
        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            print(f"✅ Lettura riuscita! Pagine totali: {len(pages)}")
            print("\n--- Anteprima (Pagina 1) ---")
            print(pages[0].page_content[:400] + "...")
        except Exception as e:
            print(f"⚠️ Errore: {e}")