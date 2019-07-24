import lorem
import os

FLAG = "LKLCTF{m4rkdown_is_co0l}"
DIR = "some-repository"

if __name__ == "__main__":
    os.chdir(DIR)
    for _ in range(73):
        j = map(ord, FLAG)

        cur_line_len = 0
        cur_line = ""
        cur_letter = next(j)
        text = ""

        try:
            while True:
                add = lorem.text().replace("\n", " ")
                for c in add:
                    cur_line += c
                    if c not in " .":
                        cur_line_len+=1
                        if cur_line_len == cur_letter:
                            text += cur_line + "\n"
                            cur_line = ""
                            cur_line_len = 0
                            cur_letter = next(j)
        except StopIteration:
            pass

        print(text)
        with open("README.md", "w") as f:
            f.write(text)
        s = lorem.sentence()
        print(s)
        os.system("git add README.md")
        os.system(f'git commit -m "{s}"')

