# Gallery Image Upload Guide

## Overview
The admin gallery endpoints now support automatic image processing with Pillow:
- ✅ Automatic thumbnail generation (400x400)
- ✅ Image optimization and resizing (max 2048x2048)
- ✅ Format conversion (RGBA → RGB for JPEG)
- ✅ File validation (type, size, extension)
- ✅ Automatic cleanup on delete/update

## API Endpoints

### Create Gallery Item (with image upload)
```http
POST /admin/gallery/
Content-Type: multipart/form-data
Authorization: Bearer <admin_token>

Form Data:
- file: (image file) [required]
- title: string [required]
- category: "Baby Showers" | "Birthdays" | "Engagements" [required]
- description: string [optional]
- tags: string (JSON array) [optional]
- display_order: integer [optional, default: 0]
- is_featured: boolean [optional, default: false]
```

### Update Gallery Item (optionally replace image)
```http
PATCH /admin/gallery/{item_id}
Content-Type: multipart/form-data
Authorization: Bearer <admin_token>

Form Data (all optional):
- file: (new image file)
- title: string
- category: string
- description: string
- tags: string
- display_order: integer
- is_featured: boolean
```

### Delete Gallery Item
```http
DELETE /admin/gallery/{item_id}
Authorization: Bearer <admin_token>
```
Automatically deletes both the main image and thumbnail from filesystem.

## Image Processing Details

### Supported Formats
- `.jpg`, `.jpeg`
- `.png`
- `.webp`

### Size Limits
- Maximum file size: **10 MB**
- Maximum dimensions: **2048 x 2048** (auto-resized)
- Thumbnail size: **400 x 400** (auto-generated)

### Optimizations
- JPEG progressive encoding
- 85% quality compression
- RGBA → RGB conversion for compatibility
- Aspect ratio preservation

## Upload Directory Structure
```
uploads/
└── gallery/
    ├── {uuid}.jpg          # Main optimized images
    ├── {uuid}.png
    └── thumbnails/
        ├── {uuid}.jpg      # Auto-generated thumbnails
        └── {uuid}.png
```

## Example: cURL Upload
```bash
curl -X POST "http://localhost:8000/admin/gallery/" \
  -H "Authorization: Bearer your_admin_token" \
  -F "file=@/path/to/image.jpg" \
  -F "title=Beautiful Birthday Party" \
  -F "category=Birthdays" \
  -F "description=Elegant outdoor birthday celebration" \
  -F "tags=[\"outdoor\", \"elegant\", \"birthday\"]" \
  -F "display_order=1" \
  -F "is_featured=true"
```

## Example: Python Upload
```python
import httpx

async def upload_gallery_image():
    url = "http://localhost:8000/admin/gallery/"
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    files = {"file": open("image.jpg", "rb")}
    data = {
        "title": "Beautiful Birthday Party",
        "category": "Birthdays",
        "description": "Elegant outdoor birthday celebration",
        "tags": '["outdoor", "elegant", "birthday"]',
        "display_order": 1,
        "is_featured": True,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, files=files, data=data)
        return response.json()
```

## Example: JavaScript/Frontend Upload
```javascript
async function uploadGalleryImage(file, formData, token) {
  const data = new FormData();
  data.append('file', file);
  data.append('title', formData.title);
  data.append('category', formData.category);
  data.append('description', formData.description);
  data.append('tags', JSON.stringify(formData.tags));
  data.append('display_order', formData.display_order);
  data.append('is_featured', formData.is_featured);

  const response = await fetch('http://localhost:8000/admin/gallery/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: data
  });

  return await response.json();
}
```

## Error Handling

### Common Errors
- **400 Bad Request**: Invalid file type, file too large, or invalid format
- **401 Unauthorized**: Missing or invalid admin token
- **404 Not Found**: Gallery item not found (update/delete)
- **500 Internal Server Error**: File processing or database error

### Example Error Responses
```json
{
  "detail": "Invalid file type. Allowed: .jpg, .jpeg, .png, .webp"
}
```

```json
{
  "detail": "File too large. Maximum size: 10MB"
}
```

## Schema Changes

### GalleryItemCreate (Updated)
Now uses Form fields instead of JSON body:
```python
class GalleryItemCreate(BaseModel):
    title: str
    description: Optional[str]
    category: Literal["Baby Showers", "Birthdays", "Engagements"]
    tags: Optional[str]  # JSON string
    display_order: int = 0
    is_featured: bool = False
    # No image_url or thumbnail_url - generated automatically!
```

## Testing the Upload

### 1. Start the Backend
```bash
cd lush-moments-backend
python -m uvicorn app.main:app --reload
```

### 2. Get Admin Token
```bash
# Login as admin
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "your_password"}'
```

### 3. Upload Test Image
```bash
curl -X POST "http://localhost:8000/admin/gallery/" \
  -H "Authorization: Bearer <token_from_step_2>" \
  -F "file=@test-image.jpg" \
  -F "title=Test Image" \
  -F "category=Birthdays"
```

### 4. View Uploaded Images
- Main image: `http://localhost:8000/uploads/gallery/{uuid}.jpg`
- Thumbnail: `http://localhost:8000/uploads/gallery/thumbnails/{uuid}.jpg`

## Dependencies Installed
- ✅ `pillow>=11.0.0` - Image processing
- ✅ `python-multipart>=0.0.9` - Multipart form data support

## Next Steps
1. Create frontend upload form for admin panel
2. Add drag-and-drop interface
3. Add image preview before upload
4. Implement batch upload functionality
5. Add image cropping/editing tools
