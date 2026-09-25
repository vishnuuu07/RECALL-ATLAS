from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[1]; themes=pd.read_csv(root/'outputs/findings.csv'); questions=pd.read_csv(root/'outputs/research_questions.csv')
lines=['# Research synthesis','',f'Candidate mechanisms: {len(themes)}. Relevant evidence mapping covers {len(questions)} required research questions.','']
for _,r in themes.sort_values('evidence_count',ascending=False).iterrows():lines.append(f"- **{r.theme}**: {r.evidence_count} relevant records, {r.source_count} source(s). {r.contradictions}")
(root/'outputs/research_summary.md').write_text('\n'.join(lines),encoding='utf-8')
print('wrote outputs/research_summary.md')
