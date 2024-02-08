def test_generate_preview(client, preview):
    response = client.get(f"/previews/preview_id/{preview.id}")
    assert response.json()["id"] == preview.id
