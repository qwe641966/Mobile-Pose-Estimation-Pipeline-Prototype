import os

os.system("touch query_image_database/database.db")
os.system("colmap/COLMAP.app/Contents/MacOS/colmap feature_extractor --database_path query_image_database/database.db --image_path query_image")