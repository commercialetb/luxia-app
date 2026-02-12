💡 LUXiA Ultimate Gold v2.0The AI-Powered Lighting Design SuiteLUXiA è un assistente intelligente per il Lighting Design che automatizza il flusso di lavoro professionale, dalla lettura della planimetria alla scelta del prodotto reale, fino alla generazione della relazione tecnica certificata.🚀 Funzionalità PrincipaliAI Vision & CAD Integration: Supporto per il caricamento di immagini (JPG/PNG), documenti PDF e file DXF (AutoCAD). Visualizzazione vettoriale del CAD direttamente nel browser.Groq Designer Agent: Utilizza i modelli Llama 3 per analizzare la geometria dei vani e suggerire la tipologia di installazione (Incasso, Sospensione, Plafone).BEGA Hunter: Connessione simulata al catalogo BEGA per l'estrazione automatica di dati fotometrici e specifiche tecniche basate sulle necessità del vano.Engine di Calcolo: Calcolo scientifico dei Lux medi ($E_{med}$) e dell'uniformità ($U_o$) basato sulla fisica della luce.Compliance Normativa: Generazione di report conformi alle specifiche UNI CEN/TS 17165:2019, UNI/TS 11999 e UNI EN 12464-1.🛠️ Requisiti di InstallazionePer far girare LUXiA in locale su Windows (PowerShell), segui questi passaggi:Clona o scarica questa cartella.Installa le dipendenze Python:PowerShellpip install -r requirements.txt
Avvia l'applicazione:PowerShellstreamlit run luxia_ultimate.py
☁️ Deploy su Streamlit CloudSe desideri pubblicare LUXiA online:Carica il codice su una repository GitHub.Connetti la repository a Streamlit Cloud.Configurazione Secret: Vai in Settings > Secrets nella dashboard di Streamlit e aggiungi la tua chiave API di Groq:Ini, TOMLGROQ_API_KEY = "gsk_tua_chiave_qui"
📂 Struttura del Progettoluxia_ultimate.py: Il cuore dell'applicazione (Interfaccia e Logica).requirements.txt: Elenco delle librerie Python necessarie.README.md: Questa guida.📜 Normative IntegrateLUXiA opera seguendo rigorosamente i protocolli europei:UNI CEN/TS 17165: Processo di progettazione illuminotecnica.UNI/TS 11999: Proprietà digitali dei prodotti (BIM ready).UNI EN 12464-1: Requisiti illuminotecnici per i posti di lavoro in interni.📝 Note per l'utente (CAD)Per una compatibilità ottimale, si consiglia di esportare i file DWG in formato DXF (ASCII) prima del caricamento. Questo permette a LUXiA di estrarre le polilinee e i layer con precisione millimetrica.

## 📚 Documentazione Tecnica

- [Formato LDT (Eulumdat)](http://www.eulumdat.org/)
- [Calcoli Illuminotecnici - UNI EN 12464-1](https://www.uni.com)
- [EZDXF Documentation](https://ezdxf.readthedocs.io/)

## 🤝 Contributi

Le pull request sono benvenute! Per grandi cambiamenti, apri prima un issue.

## 📄 Licenza

MIT License - vedi file LICENSE per dettagli

## 👨‍💻 Autore

**LUXiA Development Team**
- Versione: 1.0
- Data: Gennaio 2026

---

**Nota**: Questo software è fornito per uso preliminare/concettuale. Per progetti professionali, verificare sempre i calcoli con software specializzato certificato e normativa locale.

Notes:
------
- The .ldt parser included is a simplified heuristic for MVP purposes. It attempts to find numeric blocks and guess
  intensity distributions, but it does not replace a full photometric engine. Use it for prototyping and validation;
  for professional work consider using certified photometric tools.
- Outputs (PDF reports) are saved in the outputs/ folder.
