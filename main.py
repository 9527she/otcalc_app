from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
import json
import os
from datetime import datetime

Window.size = (360,640)

class MainLayout(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation="vertical"
        self.spacing=10
        self.padding=20

        title=Label(text="加班工资计算器",font_size=24,size_hint_y=0.08)
        self.add_widget(title)

        form=GridLayout(cols=2,spacing=8,size_hint_y=0.35)
        form.add_widget(Label(text="基本工资："))
        self.base_salary=TextInput(hint_text="输入月薪",input_filter="float")
        form.add_widget(self.base_salary)

        form.add_widget(Label(text="当月计薪天数："))
        self.work_days=TextInput(hint_text="一般21.75",input_filter="float",text="21.75")
        form.add_widget(self.work_days)

        form.add_widget(Label(text="每日加班小时："))
        self.over_hour=TextInput(hint_text="每日加班时长",input_filter="float")
        form.add_widget(self.over_hour)

        form.add_widget(Label(text="加班天数："))
        self.over_days=TextInput(hint_text="加班总天数",input_filter="float")
        form.add_widget(self.over_days)
        self.add_widget(form)

        btn_layout=BoxLayout(spacing=15,size_hint_y=0.12)
        btn_calc=Button(text="计算加班费",on_press=self.calc)
        btn_export=Button(text="导出记录",on_press=self.export_data)
        btn_layout.add_widget(btn_calc)
        btn_layout.add_widget(btn_export)
        self.add_widget(btn_layout)

        scroll=ScrollView(size_hint_y=0.45)
        self.result_label=Label(text="结果会显示在这里\n",font_size=16,valign="top")
        self.result_label.bind(size=self.result_label.setter('text_size'))
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)

        self.records=[]
        self.load_records()

    def calc(self,instance):
        try:
            base=float(self.base_salary.text)
            wd=float(self.work_days.text)
            oh=float(self.over_hour.text)
            od=float(self.over_days.text)
            hour_wage=base/(wd*8)
            over_money=hour_wage * oh * od * 1.5
            res_text=f"小时工资：{hour_wage:.2f} 元\n平日加班1.5倍\n加班费合计：{over_money:.2f} 元"
            self.result_label.text=res_text
            rec={
                "time":datetime.now().strftime("%Y-%m-%d %H:%M"),
                "base":base,
                "over_pay":over_money
            }
            self.records.append(rec)
            self.save_records()
        except:
            popup=Popup(title="提示",content=Label(text="请输入有效数字"),size_hint=(0.7,0.3))
            popup.open()

    def save_records(self):
        with open("records.json","w",encoding="utf-8") as f:
            json.dump(self.records,f,ensure_ascii=False,indent=2)

    def load_records(self):
        if os.path.exists("records.json"):
            with open("records.json","r",encoding="utf-8") as f:
                self.records=json.load(f)

    def export_data(self,instance):
        content=""
        for r in self.records:
            content += f"{r['time']} 月薪{r['base']} 加班费{r['over_pay']:.2f}\n"
        self.result_label.text="加班记录：\n"+content

class CalcApp(App):
    def build(self):
        return MainLayout()

if __name__=="__main__":
    CalcApp().run()
