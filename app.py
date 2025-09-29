from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        sleep = float(data['sleep'])
        school = float(data['school'])
        steps = int(data['steps'])
        water = int(data['water'])
        
        # Используем те же функции расчета что и в Kivy версии
        sleep_score, sleep_advice, sleep_status = calculate_sleep_score(sleep)
        school_score, school_advice, school_status = calculate_school_score(school)
        steps_score, steps_advice, steps_status = calculate_steps_score(steps)
        water_score, water_advice, water_status = calculate_water_score(water)
        
        total_score = int(sleep_score * 0.25 + school_score * 0.25 + 
                         steps_score * 0.25 + water_score * 0.25)
        
        # Формируем результат
        result = {
            'total_score': total_score,
            'details': {
                'sleep': {'value': sleep, 'status': sleep_status, 'advice': sleep_advice},
                'school': {'value': school, 'status': school_status, 'advice': school_advice},
                'steps': {'value': steps, 'status': steps_status, 'advice': steps_advice},
                'water': {'value': water, 'status': water_status, 'advice': water_advice}
            },
            'problems': []
        }
        
        # Проверяем проблемы для кнопки советов
        if sleep_status != 'optimal': result['problems'].append('СОН')
        if school_status != 'optimal': result['problems'].append('УЧЕБА')
        if steps_status != 'optimal': result['problems'].append('АКТИВНОСТЬ')
        if water_status != 'optimal': result['problems'].append('ВОДА')
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': 'Ошибка! Введите корректные числа.'})

# ТЕ ЖЕ ФУНКЦИИ РАСЧЕТА ЧТО И В KIVY
def calculate_sleep_score(sleep):
    if sleep < 6:
        return 20, '• Ложитесь на 2 часа раньше\n• Отложите телефон за 1 час до сна\n• Создайте темную атмосферу\n• Попробуйте медитацию', 'very_low'
    elif sleep < 8:
        return 70, '• Добавьте 1 час сна\n• Ложитесь в одно время\n• Избегайте кофеина вечером\n• Читайте книгу перед сном', 'low'
    elif sleep <= 10:
        return 100, '• Отлично! 8-10 часов - идеально', 'optimal'
    elif sleep <= 11:
        return 80, '• Попробуйте спать 9-10 часов\n• Больше двигайтесь днем\n• Проветривайте комнату', 'high'
    else:
        return 40, '• Установите будильник\n• Сделайте зарядку\n• Планируйте дела на утро', 'very_high'

def calculate_school_score(school):
    if school < 1:
        return 30, '• Начните с 30 минут в день\n• Составьте расписание\n• Найдите интересные темы', 'very_low'
    elif school < 3:
        return 70, '• Добавьте 1-2 часа занятий\n• Разбейте на блоки по 25 минут\n• Используйте технику Pomodoro', 'low'
    elif school <= 5:
        return 100, '• Отлично! 3-5 часов - оптимально', 'optimal'
    elif school <= 7:
        return 70, '• Снизьте нагрузку на 1-2 часа\n• Делайте перерывы каждый час\n• Занимайтесь спортом', 'high'
    else:
        return 40, '• Риск переутомления!\n• Обязательно отдыхайте\n• Чередуйте активность', 'very_high'

def calculate_steps_score(steps):
    if steps < 4000:
        return 30, '• Начните с коротких прогулок\n• Выходите на 1 остановку раньше\n• Гуляйте во время звонков', 'very_low'
    elif steps < 8000:
        return 70, '• Добавьте вечернюю прогулку\n• Ходите по лестнице\n• Танцуйте под музыку', 'low'
    elif steps <= 12000:
        return 100, '• Отлично! Идеальная активность', 'optimal'
    elif steps <= 15000:
        return 80, '• Давайте ногам отдых\n• Носите удобную обувь\n• Делайте растяжку', 'high'
    else:
        return 50, '• Чередуйте с отдыхом\n• Делайте растяжку\n• Проконсультируйтесь', 'very_high'

def calculate_water_score(water):
    if water < 3:
        return 30, '• Поставьте воду на стол\n• Пейте по стакану каждый час\n• Установите напоминания', 'very_low'
    elif water < 6:
        return 70, '• Добавьте 2-3 стакана\n• Пейте до и после еды\n• Носите воду с собой', 'low'
    elif water <= 8:
        return 100, '• Отлично! Идеальное количество', 'optimal'
    elif water <= 10:
        return 80, '• Сократите потребление\n• 6-8 стаканов достаточно', 'high'
    else:
        return 50, '• Придерживайтесь 6-8 стаканов\n• Проконсультируйтесь', 'very_high'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
