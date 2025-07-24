
import os 
import shutil 
import re 

from md_to_html import markdown_to_html_node
# from htmlnode import HtmlNode, LeafNode, ParentNode

"""
  Allowed:
    os.path.exists, os.listdir, os.path.join, os.path.isfile, os.mkdir
    shutil.copy, shutil.rmtree
  Disallowed: shutil.copytree 

"""

h1_pat = re.compile( r"^#\s(.*)$", re.M )
def extract_title(markdown):
    mtch = h1_pat.search(markdown)
    #print(f"{markdown=} {mtch=}")
    if mtch: return mtch.group(1).strip()
    raise Exception("extract_title: title in markdown is required")

def clean_public():
    try:
         shutil.rmtree("public")
         os.mkdir("public")
    except Exception as err:
        print(f"{err=}")
    

def publish_static(to_path = "public", from_path="static"):
    dir_lst, file_lst = [], []
    try:
        scan_iter = os.scandir(from_path)
        for dir_entry in scan_iter:
            if dir_entry.is_symlink(): contunue
            if dir_entry.is_dir(follow_symlinks=False):
                dir_lst.append(dir_entry.name)
                continue
            if dir_entry.is_file(follow_symlinks=False):
                file_lst.append(dir_entry.name)
                continue
    except Exception as err:
        print(f"publish_static failed scan {to_path=} {from_path=} {err=}")
    finally:
        scan_iter.close()
    try:
        for file_name in file_lst:
            shutil.copyfile(
                os.path.join(from_path, file_name),
                os.path.join(to_path  , file_name)  )
    except Exception as err:
        print(f"publish_static failed file copy {to_path=} {from_path=} {err=}")
    try:
        for dir_name in dir_lst:
            to_new = os.path.join(to_path, dir_name)
            from_new = os.path.join(from_path  , dir_name)
            print(f"new dir {to_new=} {from_new=}")
            os.mkdir(to_new)
            publish_static(to_new, from_new)
    except FileExistsError as exists_err:
        print(f"publish_static failed exists mkdir {to_path=} {from_path=} {exists_err=} {exists_err.filename=}")
    except OSError as os_err:
        print(f"publish_static failed os mkdir {to_path=} {from_path=} {os_err=}")
    except Exception as err:
        print(f"publish_static failed mkdir {to_path=} {from_path=} {err=}")
    

def gulp_file(file_name):
    file_content = ""
    with open(file_name, 'r', encoding='utf-8') as file: 
        file_content = file.read()
    return file_content
      

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path=} to {dest_path=} using {template_path=}")
    try:
        template = gulp_file(template_path)
        markdown = gulp_file(from_path)
    except FileNotFoundError as not_found_err:
        print(f"Error: The file {not_found_err.filename=} was not found. {not_found_err=}")
    except Exception as err:
        print(f"generate_page: An error occurred while reading: {err=}")
    title = extract_title(markdown)
    html_nodes = markdown_to_html_node(markdown)
    html_txt = html_nodes.to_html()
    #print(f"{html_txt=}")
    out_content = template.replace("{{ Title }}", title)
    out_content = out_content.replace("{{ Content }}", html_txt)
    #print(f"{out_content=}")
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    try:
        with open(dest_path, "w", encoding='utf-8') as file:
            file.write(out_content)
    except FileExistsError as exists_err:
        print(f"generate_page failed exists write {dest_path=} {from_path=} {exists_err=} {exists_err.filename=}")
    except OSError as os_err:
        print(f"generate_page failed os write {dest_path=} {from_path=} {os_err=}")
    except Exception as err:
        print(f"generate_page failed write {dest_path=} {from_path=} {err=}")


def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="public"):
    dir_lst, file_lst = [], []
    try:
        scan_iter = os.scandir(dir_path_content)
        for dir_entry in scan_iter:
            if dir_entry.is_symlink(): contunue
            if dir_entry.is_dir(follow_symlinks=False):
                dir_lst.append(dir_entry.name)
                continue
            if dir_entry.is_file(follow_symlinks=False):
                file_lst.append(dir_entry.name)
                continue
    except Exception as err:
        print(f"generate_pages_recursive failed scan {dest_dir_path=} {dir_path_content=} {err=}")
    finally:
        scan_iter.close()
    for file_name in file_lst:
        if not file_name.endswith(".md"): continue
        path_md_content = os.path.join(dir_path_content , file_name)
        path_html_output = os.path.join(dest_dir_path, file_name[:-3] + ".html")
        generate_page(path_md_content, template_path, path_html_output)
    for dir_name in dir_lst:
            to_new = os.path.join(dest_dir_path, dir_name)
            from_new = os.path.join(dir_path_content , dir_name)
            print(f"enerate_pages_recursiv new dir {to_new=} {from_new=}")
            generate_pages_recursive(from_new, template_path, to_new)

