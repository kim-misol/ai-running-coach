import os

# Frontend 디렉토리 경로
FRONTEND_DIR = "frontend"

files = {
    "package.json": '''
{
  "name": "ai-running-coach-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.0.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.300.0",
    "next": "latest",
    "react": "latest",
    "react-dom": "latest",
    "recharts": "^2.10.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "latest",
    "@types/react": "latest",
    "@types/react-dom": "latest",
    "autoprefixer": "^10.0.1",
    "eslint": "^9.0.0",
    "eslint-config-next": "latest",
    "postcss": "^8",
    "tailwindcss": "^3.3.0",
    "typescript": "latest"
  }
}
'''
}

def fix_package_json():
    print(f"🔧 Fixing package.json versions in '{FRONTEND_DIR}'...")

    if not os.path.exists(FRONTEND_DIR):
        print(f"❌ Error: Directory '{FRONTEND_DIR}' does not exist.")
        return

    for filename, content in files.items():
        file_path = os.path.join(FRONTEND_DIR, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
            
        print(f"  ✅ Updated: {filename} (Upgraded ESLint to v9)")

    print("\n✨ Version conflict resolved!")
    print("👉 Now run 'cd frontend && npm install' again.")

if __name__ == "__main__":
    fix_package_json()