from django.shortcuts import render
from .forms import UserForm, LoadObject, EntityCatalog
from .models import Graphic, Object
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


header = """
<header class="section page-header">
    <nav class ="fixed-top">
        <ul class="topmenu rd-navbar-nav">
          <li><a href="/"><i class="fa fa-home fa-fw"></i>Главная</a></li>
          <li><a href="/about">О нас</a></li>
          <li><a href="/get_list">Таблицы</a></li>
          <li>
            <a href="/graphics/:0">Графики</a>
            <ul class="submenu">
                <li><a href="/graphics/:1">Первый</a></li>
                <li><a href="/graphics/:2">Второй</a></li>
                <li><a href="/graphics/:3">Третий</a></li>
                <li><a href="/graphics/:4">Четвёртый</a></li>
                <li><a href="/graphics/:5">Пятый</a></li>
          </li>
        </ul>
      </nav>
</header>
"""


footer = """
<footer>
</footer>
"""


def index(request):
    form = LoadObject()
    if request.method == "POST":
        obj_id = request.POST.get("obj_id")
        try:
            cur_obj = Object.objects.get(id=obj_id)
            cur_mes = f"""
            Площадь: {cur_obj.square}
            Адрес: {cur_obj.address}
            email: {cur_obj.email_address}
            тип объекта: {cur_obj.object_type}
            """
        except ObjectDoesNotExist:
            cur_mes = "Объект не существует"
        except MultipleObjectsReturned:
            cur_mes = "Найдено более одного объекта"
    else:
        cur_mes = 'Введите искомый адрес'
    data = {"header": header, "footer": footer, "mes": cur_mes, "form": form}
    return render(request, "index.html", context=data)


def get_list(request):
    form = EntityCatalog()
    if request.method == "POST":
        entity = request.POST.get("entity")
        if entity == '1':
            bd_name = 'Объекты'
            values = Object.objects.in_bulk()
        elif entity == '2':
            bd_name = 'Графики'
            values = Graphic.objects.in_bulk()
        else:
            bd_name = 'такой сущности нет'
            values = ''
        catalog = f"""
            <p>{bd_name}</p>
        """
        for id in values:
            if entity == '1':
                ans = f"""
                <p><a href="/get_obj/:{entity}/:{id}">сущность {id}</a><p>
                <ul>
                    <li>{values[id].square}</li>
                    <li>{values[id].address}</li>
                    <li>{values[id].email_address}</li>
                    <li>{values[id].object_type}</li>
                </ul>
                """
                catalog += ans
            elif entity == '2':
                ans = f"""
                <p><a href="/get_obj/:{entity}/:{id}">сущность {id}</a><p>
                <ul>
                    <li>{values[id].cur_chartType}</li>
                    <li>{values[id].cur_dataTable}</li>
                    <li>{values[id].more}</li>
                    <li>{values[id].cur_title}</li>
                </ul>
                """
                catalog += ans
    else:
        catalog = ''
    data = {"header": header, "footer": footer, "catalog": catalog, "form": form}
    return render(request, "get_list.html", context=data)


def obj(request, n, obj_id):
    if n == ':1':
        h1 = 'Объекты'
        cur_obj = Object.objects.get(id=int(obj_id[1:]))
        cur_mes = f"""
        Площадь: {cur_obj.square}
        Адрес: {cur_obj.address}
        email: {cur_obj.email_address}
        тип объекта: {cur_obj.object_type}
        """
    elif n == ':2':
        h1 = 'Графики'
        cur_obj = Graphic.objects.get(id=int(obj_id[1:]))
        cur_mes = f"""
        {cur_obj.cur_chartType}
        {cur_obj.cur_dataTable}
        {cur_obj.more}
        {cur_obj.cur_title}
        """
    else:
        h1 = 'что-то не так'
        cur_obj = ''
    data = {"header": header, "footer": footer, "h1": h1, "catalog": cur_mes}
    return render(request, "obj.html", context=data)


def about(request):
    if request.method == "POST":
        cur_mes = 'Данные отправлены на сервер и добавлены в БД'
        cur_square = request.POST.get("square")
        cur_address = request.POST.get("address")
        cur_email_address = request.POST.get("email_address")
        object_type = request.POST.get("type")
        new_object = Object.objects.create(square=cur_square, address=cur_address,
                                           email_address=cur_email_address, object_type=object_type)
        gr = Graphic.objects.get(id=2)
        cur_data = gr.cur_dataTable
        cur_data = cur_data[1:-1]
        cur_data = cur_data.split('[')
        c1 = int(cur_data[2][15:-2])
        c2 = int(cur_data[3][13:-2])
        c3 = int(cur_data[4][8:-1])
        if object_type == '1':
            c1 += 1
        elif object_type == '2':
            c2 += 1
        elif object_type == '3':
            c3 += 1
        gr.cur_dataTable = f"[['Типы недвижимости','Количество'],['Коммерческая',{c1}],['Загородная',{c2}],['Жилая',{c3}]]"
        gr.save(update_fields=["cur_dataTable"])
    else:
        cur_mes = 'Заполните форму для загрузки данных в бд'
    form = UserForm()
    data = {"header": header, "footer": footer, "mes": cur_mes, "form": form}
    return render(request, "about.html", context=data)


def graphics(request, graphics_id):
    if graphics_id != ':0':
        cur_graphic = Graphic.objects.get(id=int(graphics_id[1]))
        cur_chartType = cur_graphic.cur_chartType
        cur_dataTable = cur_graphic.cur_dataTable
        more = cur_graphic.more
        cur_title = cur_graphic.cur_title
        js_script = f"""
            <script type='text/javascript'>
              function drawVisualization() {{
                var wrapper = new google.visualization.ChartWrapper({{
                  chartType: '{cur_chartType}',
                  dataTable: {cur_dataTable},
                  options: {{
                    {more}
                    'title': '{cur_title}'
                  }},
                  containerId: 'vis_div'
                }});
                wrapper.draw();
              }}
            </script>
        """
    else:
        js_script = ''
    h1 = 'Графики'
    mes = ''
    data = {"header": header, "footer": footer, "get_graphic": js_script, "h1": h1, "mes": mes}
    return render(request, "graphics.html", context=data)
