import os
import yaml

Tag_list = []

def extract_tags(path):
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if filename == "TagManager.asset":
                fname = os.path.join(dirpath, filename)
                skip_lines = 3
                with open(fname) as f:
                    for i in range(skip_lines):
                        _ = f.readline()
                    fruits_list = yaml.load(f, Loader=yaml.FullLoader)
                    di = fruits_list.get('TagManager')
                    tags_list = di.get('tags')
                    return tags_list
    else:
        tags_list = 0


def tags_dict(path):
    tags_list = extract_tags(path)
    new_tag_dict = {}
    for i in range(len(tags_list)):
        new_tag_dict["m_TagString: " + tags_list[i]] = "m_TagString: Tag " + str(i)
    return new_tag_dict


def tags_manager_dict(path):
    tags_list = extract_tags(path)
    tag_manager_dict = {}
    for i in range(len(tags_list)):
        tag_manager_dict["  - Tag " + str(i) + "\n"] = "  - " + tags_list[i] + "\n"
    return tag_manager_dict


def initial_tags_dic(path):
    tags_list = extract_tags(path)
    tags_dict = {}
    for i in range(len(tags_list)):
        tags_dict["Tag " + str(i)] = tags_list[i]
    return tags_dict


def update_files(path):
    file_path_list = []

    Tag_dict = tags_dict(path)

    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.unity') or filename.endswith('.prefab'):
                fname = os.path.join(dirpath, filename)
                file_path_list.append(fname)

    for file in file_path_list:
        for key, value in Tag_dict.items():
            # For Reading file data
            f_open = open(file, "rt")
            data = f_open.read()
            data = data.replace(key, value)
            f_open.close()

            # For Writing replaced data
            f_open = open(file, "wt")
            f_open.write(data)
            f_open.close()
    
    Create_tags_txt_file(path)
    Update_tag_manager(path)


def convert_yaml_to_txt(temp_data, path):
    tags_list = extract_tags(path)
    Tag_man_dict = tags_manager_dict(path)
    Tag_index = 0
    for index, name in enumerate(temp_data):
        if name == '  tags:\n':
            Tag_index = index

        for i in range(1, len(tags_list) + 1):
            for key, value in Tag_man_dict.items():
                if temp_data[Tag_index + i] == value:
                    temp_data[Tag_index + i] = key

    data = ""
    for i in temp_data:
        data += i

    return data


def Update_tag_manager(path):
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if filename == "TagManager.asset":
                fname = os.path.join(dirpath, filename)

                f_open = open(fname, "rt")
                temp_data = f_open.readlines()
                f_open.close()

                data = convert_yaml_to_txt(temp_data, path)

                # For Writing replaced data
                f_open = open(fname, "wt")
                f_open.write(data)
                f_open.close()


def Create_tags_txt_file(path):
    tags = initial_tags_dic(path)
    file_creation_path = path + "/Assets/TagsList.txt"
    f = open(file_creation_path, 'w+')
    for key, value in tags.items():
        tagss = key + " : " + value + "\n"
        f.write(tagss)
    f.close()


if __name__ == '__main__':
    dir_path = input("Enter game folder path : ")
    update_files(dir_path)
