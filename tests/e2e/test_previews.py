def test_generate_preview(client, preview):
    response = client.get(f"/previews/preview_id/{preview.id}")
    assert not response.json(["title"]).startswith('"')
    assert not response.json(["title"]).endswith('"')
    assert response.json()["title"] == preview.title
    assert response.json()["id"] == preview.id
