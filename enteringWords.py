import json
import flet
from flet import (
    Page,
    DataTable,
    DataColumn,
    Text,
    DataRow,
    DataCell,
    TextField,
    Row,
    Column,
    Icon, 
    Tabs,
    Tab
)

def create_entering_page(page: Page):
    with open('words.json', encoding='utf-8') as w:
        words = json.load(w)
    
    wordsData = DataTable(
        columns=[
                DataColumn(Text("단어")),
                DataColumn(Text("뜻")),
            ],
        rows = [
            
        ]
    )
    
    for word in words["activated"]:
        if word and isinstance(word["meaning"], str):
            wordsData.rows.append(DataRow(
                cells= [
                    DataCell(Text(word["word"])),
                    DataCell(Text(word["meaning"]))
                ]
            ))
        elif word and isinstance(word["meaning"], list):
            wordsData.rows.append(DataRow(
                cells= [
                    DataCell(Text(word["word"])),
                    DataCell(Text(", ".join(word["meaning"])))
                ]
            ))
    
    def close_banner(e):
        page.banner.open = False
        page.update()
    
    page.banner = flet.Banner(
        bgcolor=flet.colors.GREEN_100,
        leading=Icon(flet.icons.CHECK_ROUNDED, color=flet.colors.LIGHT_GREEN_400, size=40),
        content=Text(
            "데이터베이스에 저장 완료!"
        ),
        actions=[
            flet.TextButton("확인", on_click=close_banner),
        ],
    )
        
    def meaningDevider(meaning: str):
        meanings = meaning.value.split(',')
        for m in range(len(meanings)):
            meanings[m] = meanings[m].replace(" ", "")
        return meanings
    
    def isExist(word):
        with open("words.json", 'r', encoding='utf-8') as w:
            words = json.load(w)
            for w in words["activated"]:
                if w["word"] == word:
                    return True
        return False
    
    def btnClick(e):
        w = word.value
        m = meaningDevider(meaning)
        if not isExist(w):
            container = dict()
            container["word"] = w
            container["meaning"] = m
            container["memoCount"] = 0
            words["activated"].append(container)
            wordsData.rows.append(DataRow(
                cells= [
                    DataCell(Text(word.value)),
                    DataCell(Text(meaning.value))
                ]
            ))
            
        word.value = ""
        word.update()
        meaning.value = ""
        meaning.update()
        word.focus()
        page.update()
    
    def save(e):
        with open('words.json', 'w', encoding='utf-8') as w:
            json.dump(words, w, indent='\t', ensure_ascii=False)
        page.banner.open = True
        page.update()
        
        
        
    titleForInput = Text("공부할 단어 입력", style=flet.TextThemeStyle.TITLE_LARGE)
    word = TextField(label="단어", width=300, autofocus=True)
    meaning = TextField(label="뜻", width=300)
    btn = flet.ElevatedButton("Submit", on_click=btnClick)
    btnSave = flet.FilledButton("Save", icon="add", on_click=save)
    
    return Tabs(
        selected_index=0,
        animation_duration=0,
        scrollable=False,
        tabs= [
            Tab(
                text = "단어 입력",
                icon = flet.icons.INPUT_ROUNDED,
                content = Column(
                    controls=[
                        titleForInput,
                        word,
                        meaning,
                        Row(
                            controls=[
                                btn,
                                btnSave
                            ]
                        )
                    ],
                    expand=True,
                )
            ),
            Tab(
                text="단어 보기",
                icon=flet.icons.ABC_ROUNDED,
                content=wordsData
            )
        ]
    )