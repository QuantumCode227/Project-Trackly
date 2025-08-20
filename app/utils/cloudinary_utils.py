def extract_public_id(url: str):
    """Extract public_id from Cloudinary URL"""
    splitted_list = url.split("/")
    public_id = f"{splitted_list[-2]}/{splitted_list[-1].split('.')[0]}"
    return public_id
