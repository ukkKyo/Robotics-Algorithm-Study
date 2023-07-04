from typing import List, Dict, Union
from urllib import request, error
import yaml
import json
import ssl


def get_user_github_id(username: str) -> str:
    assert type(username) == str

    try:
        url = f"https://api.github.com/users/{username}"
        ssl_context = ssl._create_unverified_context()
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        text = request.urlopen(req, context=ssl_context).read().decode('utf8')
        data = json.loads(text)
    except error.HTTPError:
        raise Exception(f"There is no `{username}` user.")
    return data['id']


def make_member_table(members: List[Dict[str, str]]) -> List[str]:
    num_of_members: int = len(members)

    lines: List[str] = []

    lines.append("## RAS Members 👩‍👩‍👧‍👦")
    lines.append("<table>")
    for i in range(0, num_of_members, 5):
        # Image
        lines.append("<tr height=\"140px\">")
        for member in members[i: i+5]:
            lines.append("<td align=\"center\" width=\"130px\">")
            name: Union[str, None] = member.get('name', None)
            github_name: Union[str, None] = member.get('github', None)
            github_id: Union[str, None] = get_user_github_id(github_name)
            lines.append(
                f"<a href=\"https://github.com/{github_name}\"><img height=\"100px\" width=\"100px\" src=\"https://avatars.githubusercontent.com/u/{github_id}?v=4\"/></a> <br />"
            )
            lines.append(
                f"<a href=\"https://github.com/{github_name}\">{name}</a>"
            )
            lines.append("</td>")
        lines.append("</tr>")

        # Badge
        lines.append("<tr height=\"50px\">")
        for member in members[i: i+5]:
            baekjoon_name: Union[str, None] = member.get('baekjoon', None)
            lines.append(f"<td align=\"center\">")
            if baekjoon_name is not None:
                lines.append(f"<img src=\"http://mazassumnida.wtf/api/mini/generate_badge?boj={baekjoon_name}\" />")
                lines.append(f"<br />")
                lines.append(f"<a href=\"https://www.acmicpc.net/user/{baekjoon_name}\">Baekjoon</a>")
                lines.append(f"<br />")
                lines.append(f"<a href=\"https://solved.ac/profile/{baekjoon_name}\">solved.ac</a>")
            lines.append("</td>")
        lines.append("</tr>")
    lines.append("</table>")
    
    lines: List[str] = [f"{x.rstrip()}\n" for x in lines]

    return lines


def make_readme():
    header_text: List[str] = open('header.md', 'r').readlines()
    members: Dict[str, List[Dict[str, str]]] = yaml.load(open('members.yaml', 'r'), Loader=yaml.FullLoader)

    member_text: List[str] = make_member_table(members['member'])

    blanks: List[str] = ['\n\n']
    all_text: List[str] = header_text + blanks + member_text
    with open('README.md', 'w') as f:
        f.writelines(all_text)
        f.close()


if __name__ == "__main__":
    make_readme()
