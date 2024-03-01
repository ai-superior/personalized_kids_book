def test_generate_preview(client, preview):
    response = client.get(f"/previews/preview_id/{preview.id}")
    assert not response.json()["title"].startswith('"')
    assert not response.json()["title"].endswith('"')
    assert response.json()["title"] == preview.title
    assert response.json()["id"] == preview.id


def test_temp_preview(client):
    payload = {
        "order_id": "b16c5834-e34f-4f6f-9280-6337393c160f",
        "asset_ids": [
            "ad486c34-3718-42d0-91fe-b823b7d002ae",
            "8d1972b3-7a12-4334-b34c-0a4f83a15933",
            "c8034cab-a1b4-43cb-859f-c64661df0d8c",
        ],
    }
    response = client.post(f"/previews", json=payload)
    assert True
