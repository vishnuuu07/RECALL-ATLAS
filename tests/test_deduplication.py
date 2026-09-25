from pipeline.deduplicate import deduplicate
def test_exact_hash_duplicate_removed():
    out,n=deduplicate([{'content_hash':'a'},{'content_hash':'a'},{'content_hash':'b'}]);assert len(out)==2 and n==1
