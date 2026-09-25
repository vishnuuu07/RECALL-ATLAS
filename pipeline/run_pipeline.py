from __future__ import annotations
import argparse,json,sys
from datetime import datetime,timezone
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from collectors.generic_import import load
from collectors.app_store import collect
from pipeline.schema import SourceRecord
from pipeline.normalize import clean,content_hash
from pipeline.deduplicate import deduplicate
from pipeline.relevance import classify
from pipeline.extract import enrich
from pipeline.audit import validate
from pipeline.aggregate import questions,themes,hypotheses
from pipeline.publish import publish
from pipeline.workbook_import import import_workbook,overlap_report
from recall_atlas.metrics import funnel

def main():
 p=argparse.ArgumentParser();p.add_argument('--app-store-pages',type=int,default=1);p.add_argument('--include-app-store',action='store_true',help='Explicitly opt into transient App Store collection.');args=p.parse_args()
 raw=[]
 for raw_file in sorted((ROOT/'data/raw').glob('*_public_records.jsonl')):
  raw.extend(load(raw_file))
 if args.include_app_store:
  for page in range(1,args.app_store_pages+1):
   try: raw.extend(collect(page))
   except Exception as exc: print(f'Apple App Store page {page} unavailable: {exc}',file=sys.stderr)
 for r in raw:
  SourceRecord(**r);r['original_text']=clean(r['original_text']);r['public_excerpt']=clean(r['public_excerpt']);r['content_hash']=content_hash(r['original_text'])
 records,removed=deduplicate(raw);errors=validate(records)
 if errors: raise SystemExit('; '.join(errors))
 for r in records:
  original_label,original_depth,original_confidence=classify(r['original_text'],legacy=True)
  label,depth,confidence=classify(r['original_text'])
  r.update(relevance_original=original_label,evidence_depth_original=original_depth,confidence_original=original_confidence,
           relevance=label,evidence_depth=depth,confidence=confidence,
           classification_correction=(f'{original_label}/{original_depth} → {label}/{depth}' if (original_label,original_depth)!=(label,depth) else 'No change'))
  r.update(enrich(r['original_text']))
 try:
  from pipeline.embed import embed
  from pipeline.cluster import cluster
  vectors,model=embed([r['original_text'] for r in records]); labels=cluster(vectors)
  for r,label in zip(records,labels):r['semantic_cluster']=int(label)
 except Exception as exc:
  model=f'not executed ({type(exc).__name__})'
  for r in records:r['semantic_cluster']=None
 evidence=pd.DataFrame(records); theme_df=themes(evidence); question_df=questions(evidence); hypothesis_df=hypotheses(theme_df); funnel_df=funnel(evidence,len(raw))
 imported_cases,consolidated_cases,overlap_audit,workbook_meta=import_workbook(evidence,ROOT/'data/raw')
 corrections=int((evidence.classification_correction!='No change').sum())
 meta={'dataset_version':'0.4.0','schema_version':'1.2','pipeline_version':'0.4.0-workbook-import','collection_timestamp':datetime.now(timezone.utc).isoformat(),'processing_timestamp':datetime.now(timezone.utc).isoformat(),'raw_record_count':len(raw),'duplicates_removed':removed,'unique_record_count':len(records),'classification_correction_count':corrections,'ai_model_version':model,'ai_processing':'Deterministic, audit-preserving evidence classification and taxonomy; offline pretrained sentence embeddings + KMeans when model execution succeeds; no LLM extraction.','audit_status':'Automated provenance/schema/deduplication/reconciliation checks passed. Original and corrected labels are retained; independent human-label accuracy is unmeasured. Public views omit source links and platform identifiers.'}
 meta.update(workbook_meta)
 publish(consolidated_cases,theme_df,question_df,hypothesis_df,funnel_df,meta,{'imported_retrieval_cases':imported_cases,'retrieval_cases':consolidated_cases,'case_overlap_audit':overlap_audit})
 out=ROOT/'outputs';out.mkdir(exist_ok=True);theme_df.to_csv(out/'findings.csv',index=False);question_df.to_csv(out/'research_questions.csv',index=False);hypothesis_df.to_csv(out/'hypothesis_matrix.csv',index=False)
 consolidated_cases.groupby('record_kind').agg(records=('case_id','count'),recorded_outcomes=('outcome_classification',lambda x:int(x.str.contains('Found',case=False,na=False).sum()))).reset_index().to_csv(out/'source_health.csv',index=False)
 (out/'duplicate_overlap_report.md').write_text(overlap_report(overlap_audit,workbook_meta),encoding='utf-8')
 print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
