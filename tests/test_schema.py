from pipeline.schema import SourceRecord
def test_source_schema_accepts_minimal_record():
    r=SourceRecord(record_id='x',source_platform='Test',source_type='test',source_url='https://example.com',collected_at='2026-01-01T00:00:00Z',original_text='a',public_excerpt='a',collection_query='q',collection_method='m',collection_batch='b')
    assert r.record_id=='x'
