import sys
import json
import urllib.request
import bs4 as bs
import os

options = ['dynamic-programming', 'gcd', 'ad-hoc-1', 'graph-theory', 'graph', 'math', 'number-theory', 'tree', 'adhoc', 'bfs', 'binary-search']


def readJson():
    with open('settings.json') as json_data:
        data = json.load(json_data)
        return data

def writeJson(updataed_data):
    with open('settings.json', 'w') as json_data:
        json_data.write(json.dumps(updataed_data, indent=4, sort_keys=True))


args = sys.argv
json_data = readJson()


def page(tag):
    url = 'http://www.spoj.com/problems/tag/'
    url = url + tag
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    completed_problems = json_data['Completed']
    for data in soup.find_all('tbody'):
        for a in data.find_all('a'):
            if '/problems/' in a.get('href'):
                problem = 'http://www.spoj.com' + a.get('href')
                if problem not in completed_problems:
                    questionGenerate(problem)
                    return
    print("----All questions from this tag are solved----")


def questionGenerate(problem_url):
    try:
        sauce = urllib.request.urlopen(problem_url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        title = soup.title.text
        title = title[19:len(title)]
        question = soup.find("div", {"id": "problem-body"}).text
        text = '/*' + title + '\n' + problem_url + '\n' + question + '*/'
        print(problem_url)
        json_data["Completed"].append(problem_url)
        writeJson(json_data)
    except:
        print("Invalid tag")
        return
    createFile(title, text)

def createFile(title, text):
    try:
        dir = json_data['Path']
        file_name = title + json_data['Extension']
        file_path = dir + '\\' + file_name
        f = open(file_path, 'w', encoding="utf8")
        f.write(text)
        f.close()
    except:
        print("Directory not found")

if len(args) == 1 or args[1] == '--help' or args[1] == '--h':
    print('Usage:')
    print(' python downloader.py <command> [options]')
    print('\nCommands:\n'
          ' setting\t\t\tShows configuration data\n'
          ' download\t\t\tDownload a question\n'
          ' setPath\t\t\tSet file creation directory location\n'
          ' tags\t\t\t\tShows all tags\n'
          ' addTags\t\t\tAdd a new tag\n'
          ' setExtension\t\t\tSet file extension(add . at beginning)\n')
    print('General options:\n'
          ' -h, --help\t\t\tshows all commands and options\n'
          ' -about\t\t\t\tshows about this project')

elif args[1] == 'setting':
    data = readJson()
    print(json.dumps(data, indent=4, sort_keys=True))
elif args[1] == 'setPath':
    path = args[2]
    if not os.path.exists(path):
        os.makedirs(path)
    json_data['Path'] = path
    writeJson(json_data)
elif args[1] == 'setExtension':
    Extension = args[2]
    json_data['Extension'] = args[2]
    writeJson(json_data)
elif args[1] == 'option':
    print(options)
elif args[1] == 'download':
    tag = args[2]
    page(tag)
elif args[1] == 'addTag':
    options.append(args[2])
elif args[1] == 'about':
    print('----------SPOJ QUESTION DOWNLOADER----------\n'
          ' Siddharth Nayak\n'
          ' https://github.com/siddharth1297/SpojQuestionDownloader')
