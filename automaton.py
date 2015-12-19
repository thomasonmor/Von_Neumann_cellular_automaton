#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Коды состояний (можно оптимизировать)
#Вакуум, нулевое состояние
U = 0
#Транзитная клетка
S = 1
S0 = 2
S00 = 3
S01  = 4
S000 = 5
S1  = 6
S10 = 7
S11 = 8
#Конфлуэнтная клетка
C00 = 9
C10 = 10
C01 = 11
C11 = 12
#Обычные передающие
T00 = 13  #>
T01 = 14  #^
T02 = 15  #<
T03 = 16  #v
#Обычные передающие возбуждённые
E00 = 17  #>*
E01 = 18  #^*
E02 = 19  #<*
E03 = 20  #v*
#Специальные передающие
T10 = 21  #>
T11 = 22  #^
T12 = 23  #<
T13 = 24  #v
#Специальные передающие возбуждённые
E10 = 25  #>*
E11 = 26  #^*
E12 = 27  #<*
E13 = 28  #v*
#Функция обновления состояния клетки
def update(prev_state, up,down,left,right):
  #Однобуквенные имена для удобства
  p = prev_state
  u = up
  d = down
  l = left
  r = right
  #Правила для обычных стрелок
  #Стрелка становится возбуждённой если в любой из трёх "входных сторон"
  #(входные стороны стрелки это те стороны в которые она не указыает)
  #есть возбуждённая стрелка направленная к ней,
  #либо если в любой из трёх входных сторон есть конфлуэнтная клетка в возбуждённых состояниях CC10 или CC11
 
  r_std_exc = (r == E02) or (r == CC10) or (r == CC11)
  u_std_exc = (u == E03) or (u == CC10) or (u == CC11)
  l_std_exc = (l == E00) or (l == CC10) or (l == CC11)
  d_std_exc = (d == E01) or (d == CC10) or (d == CC11)
 
  uld_std_exc = u_std_exc or l_std_exc or d_std_exc
  dlr_std_exc = d_std_exc or l_std_exc or r_std_exc
  dur_std_exc = d_std_exc or u_std_exc or r_std_exc
  ulr_std_exc = u_std_exc or l_std_exc or r_std_exc
 
  if p == T00 and uld_std_exc:
    return E00
  if p == T01 and dlr_std_exc:
    return E01
  if p == T02 and dur_std_exc:
    return E02
  if p == T03 and ulr_std_exc:
    return E03
  #Стрелка перестаёт быть возбуждённой если на неё не указывает ни одна возбуждённая клетка
  if p == E00 and not uld_std_exc:
    return E00
  if p == E01 and not dlr_std_exc:
    return E01
  if p == E02 and not dur_std_exc:
    return E02
  if p == E03 and not ulr_std_exc:
    return E03
 
  #Правила для специальных клеток
  #Аналогичны правилам для обычных клеток
  r_sp_exc = (r == E12) or (r == CC10) or (r == CC11)
  u_sp_exc = (u == E13) or (u == CC10) or (u == CC11)
  l_sp_exc = (l == E10) or (l == CC10) or (l == CC11)
  d_sp_exc = (d == E11) or (d == CC10) or (d == CC11)
 
  uld_sp_exc = u_sp_exc or l_sp_exc or d_sp_exc
  dlr_sp_exc = d_sp_exc or l_sp_exc or r_sp_exc
  dur_sp_exc = d_sp_exc or u_sp_exc or r_sp_exc
  ulr_sp_exc = u_sp_exc or l_sp_exc or r_sp_exc
 
  if p == T10 and uld_sp_exc:
    return E10
  if p == T11 and dlr_sp_exc:
    return E11
  if p == T12 and dur_sp_exc:
    return E12
  if p == T13 and ulr_sp_exc:
    return E13
  #Стрелка перестаёт быть возбуждённой если на неё не указывает ни одна возбуждённая клетка
  if p == E10 and not uld_sp_exc:
    return E10
  if p == E11 and not dlr_sp_exc:
    return E11
  if p == E12 and not dur_sp_exc:
    return E12
  if p == E13 and not ulr_sp_exc:
    return E13
 
  #Правила уничтожения передающих клеток:
  #Если рядом с любой обычной передающей клеткой есть специальная передающая возбуждённая,
  #указывающая на неё то обычная передающая уничтожается и заменяется вакумом (U)
  #И наоборот, любая обычная передающая возбуждённая направленная в специальную уничтожает её
 
  any_sp_exc = r_sp_exc or u_sp_exc or l_sp_exc or d_sp_exc
  any_std_exc = r_std_exc or u_std_exc or l_std_exc or d_std_exc
 
  if p in [T01,T02,T03,T04,E01,E02,E03,E04] and any_sp_exc:
    return U
  if p in [T11,T12,T13,T14,E11,E12,E13,E14] and any_std_exc:
    return U
 
  #Правила развития транзитных состояний
  #Транзитное состояние S возникает в пустой клетке если в неё направлена любая возбуждённая стрелка.
  #Далее в зависимости от поступающих сигналов транзитная клетка изменяет состояния в конце концов превращаясь в одну из девяти типов клеток
 
  any_exc = (any_sp_exc or any_std_exc)
 
  if p == U and any_exc:
    return S
 
  if p == S:
    if any_exc:
      return S1
    else:
      return S0
 
  if p == S0:
    if any_exc:
      return S01
    else:
      return S00
 
  if p == S00:
    if any_exc:
      return T02
    else:
      return S000
 
  if p == S000:
    if any_exc:
      return T01
    else:
      return T00
 
  if p == S01:
    if any_exc:
      return T10
    else:
      return T03
 
  if p == S1:
    if any_exc:
      return S10
    else:
      return S11
     
  if p == S10:
    if any_exc:
      return T12
    else:
      return T11
     
  if p == S11:
    if any_exc:
      return C00
    else:
      return T13
 
  #Конфлуэнтные клетки
  #Конфлуэнтная клетка задерживает проходящий через неё сигнал на два такта:
  #при поступлении сигнала сначала переходит в состояние C01 а потом в возбуждённые состояния C10 или C11 если был ещё один входной сигнал.
  #Конфлуэнтная клетка принимает входной сигнал (переходит в C01 из C00 или в С11 из С01) только если все направленные в неё обычные передающие стрелки возбуждены.
  #Конфлуэнтная клетка выдаёт выходной сигнал на обычные или специальные передающие стрелки направленные к ней любой стороной кроме выхода,
  #когда находится в состояниях C10 или C11.
  #Если рядом с конфлуэнтной клеткой находится хоть одна специальная передающая стрелка направленная в неё то конфлуэнтная клетка уничтожается, переходя в ваккуум (U)
 
  r_std_exc = (r == E02)
  u_std_exc = (u == E03)
  l_std_exc = (l == E00)
  d_std_exc = (d == E01)
 
  r_std_ne = (r == T02)
  u_std_ne = (u == T03)
  l_std_ne = (l == T00)
  d_std_ne = (d == T01)
 
  #Рассчитываем сколько входных возбуждённых и невозбуждённых стрелок у данной конфлуэнтной клетки
  input_exc = 0
  input_nonexc = 0
 
  if r_std_exc:
    input_exc += 1
  if u_std_exc:
    input_exc += 1
  if l_std_exc:
    input_exc += 1
  if d_std_exc:
    input_exc += 1
  if r_std_ne:
    input_nonexc += 1
  if u_std_ne:
    input_nonexc += 1
  if l_std_ne:
    input_nonexc += 1
  if d_std_ne:
    input_nonexc += 1
 
  #Условие возбуждени конфлуэнтной клетки
  con_input_excite = False
  if input_exc > 0 and input_nonexc == 0:
    con_input_excite = True
 
  #Обновляем клетку реализуя запаздывание, память хранится в
  if p == C00 and con_input_excite:
    return C01
 
  if p == C01 and con_input_excite:
    return C11
  else:
    return C10
 
  if p == C10 and con_input_excite:
    return C01
  else:
    return C00
   
  if p == C11 and con_input_excite:
    return C11
  else:
    return C10
 
  #Уничтожение конфлуэнтных клеток
  if p in [C00,C01,C10,C11] and any_sp_exc:
    return U
k = 4
color_table = []
        pygame.time.wait(10)
        window.fill((0,0,0))
        pygame.display.flip()
        react_to_events()
def VNA_init(H,W):
    [U]*W*H
def run_automata(dim, limit, initial_fn, update_fn, draw_fn):
    N = 0
    initial = initial_fn()
    flag = 0
    state = [initial,initial[:]]
    while N < limit:
        N = N + 1
        draw_fn()
        if flag == 0:
            update_fn(state[0], state[1])
            flag = 1
        else:
            update_fn(state[1], state[0])
            flag = 0
