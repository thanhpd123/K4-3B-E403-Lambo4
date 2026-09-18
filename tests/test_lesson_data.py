from codebase.lesson_data import lesson_catalog, review_context


def test_catalog_maps_two_real_slide_decks():
    catalog = lesson_catalog()
    assert {item["id"] for item in catalog} == {"day1-foundation", "day2-problem"}
    assert all(item["slide_count"] == 29 for item in catalog)


def test_review_context_starts_with_current_slide_and_related_transcript():
    chunks = review_context("day1-foundation", 4, "Generative AI sinh ra văn bản")
    assert chunks[0].source_type == "slide"
    assert chunks[0].source_id == "Slide 4"
    assert any(chunk.source_type == "transcript" for chunk in chunks[1:])
