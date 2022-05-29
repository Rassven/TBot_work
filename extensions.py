import requests
import json
from config import ru_c_dict, ru_err_mess, ru_greeting_mess, ru_help_mess

err_message = ''
base, target, amount = '', '', '1'


class UserException(Exception):
    def __init__(self, r_str):
        global err_message
        err_message = 'Ошибка! ' + r_str


class Converter:
    @staticmethod
    def convert(pars):
        global err_message, base, target, amount
        save_fl = 'set'
        if base == '' or target == '' or amount == '':
            save_fl = 'not set'
        try:
            if pars == '/mem' and save_fl == 'not set':
                raise UserException(ru_err_mess['input'][5] + '\n' + 'нажми /help')
        except UserException:
            result_text = err_message
            return result_text

        if pars != '/mem':
            # tst_str = 'эфириум перевести в 129 биткоинов и доллары или евро или рубли'; pars = tst_str
            # разборка строки
            temp = pars[1:].lower()
            words = temp.split()
            fpar = []
            num = -1

            for wcou in words:
                if wcou.isnumeric():
                    num = float(wcou)
                    break
            for wcou in words:
                for check_val in ru_c_dict:
                    if wcou.find(check_val) > -1:
                        fpar.append(check_val)
                        break


            # Обработка поиска
            try:
                if len(words) > 3 and len(fpar) == 0:
                    raise UserException(ru_greeting_mess[2])
            except UserException:
                result_text = err_message
                return result_text

            try:
                if len(fpar) == 0 and num == -1:
                    raise UserException(ru_err_mess['input'][0])
                if len(fpar) > 2:
                    raise UserException(ru_err_mess['input'][1])
                if amount == '' and num < 0:
                    raise UserException(ru_err_mess['input'][4])
            except UserException:
                result_text = err_message
                return result_text

            #Обработка данных
            if num > -1:
               amount = str(num)
            try:
                if len(fpar) == 1:
                    if base == fpar[0]:
                        raise UserException(ru_err_mess['conversion'][0])
                    else:
                        target = fpar[0]
                else:
                    base = fpar[0]
                    target = fpar[1]
            except UserException:
                result_text = err_message
                return result_text
        #else:
            #конвертация

        test = str(amount)
        amount_s = test[0:test.find('.') + 4]


        #сборка
        base_ticker = ru_c_dict[base][0]
        target_ticker = ru_c_dict[target][0]
        # Запрос: fsym=USD&tsyms=RUB, ответ: {"RUB": 63.93}
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={target_ticker}')
        result = float(amount) * json.loads(r.content)[target_ticker]
        ending = 3

        test = str(result)
        result_s = test[0:test.find('.') + 4]

        result_text = f'Стоимость {amount_s} {base + ru_c_dict[base][ending]} составляет {result_s} {target + ru_c_dict[target][ending]}'
        return result_text
