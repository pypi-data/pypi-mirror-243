# Author: Salyl Bhagwat, Gammath Works
# Copyright (c) 2021-2023, Salyl Bhagwat, Gammath Works
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__author__ = 'Salyl Bhagwat'
__copyright__ = 'Copyright (c) 2021-2023, Salyl Bhagwat, Gammath Works'

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from mdptoolbox import mdp
import gymnasium as gym

try:
    from gammath_spot import gammath_utils as gut
except:
    import gammath_utils as gut

def find_index(start_index, end_index, item, vals):
    bottom = start_index
    top = end_index
    found_index = -1

    while (bottom <= top):
        middle = (bottom + top)//2
        #Get df date at mid-index
        val = vals[middle]
        if (val == item):
            found_index = middle
            break
        else:
            if (val > item):
                bottom = (middle + 1)
            else:
                top = (middle - 1)

    return found_index

def periodic_min_max(tsymbol, path, sh_gscores, prices):
    size = len(sh_gscores)
    df = pd.DataFrame(columns=['MIN', 'MIN_INDEX', 'PP', 'MAX', 'MAX_INDEX', 'DP'], index=range(int(size/63)))
    tri_monthly_offset = (size%63)
    i = 0
    while (tri_monthly_offset < size):
        end_index = (tri_monthly_offset+63)
        subset = sh_gscores[tri_monthly_offset:end_index]
        min_index = np.argmin(subset)
        max_index = np.argmax(subset)
        min_index += tri_monthly_offset
        max_index += tri_monthly_offset


        df.MIN[i] = sh_gscores[min_index]
        df.MIN_INDEX[i] = min_index
        df.PP[i] = prices[min_index]
        df.MAX[i] = sh_gscores[max_index]
        df.MAX_INDEX[i] = max_index
        df.DP[i] = prices[max_index]
        i += 1
        tri_monthly_offset += 63
        print(f'min: {sh_gscores[min_index]}, index: {min_index}, Price: {prices[min_index]} max: {sh_gscores[max_index]}, index: {max_index}, Price: {prices[max_index]}, Distance: {abs(max_index-min_index)}')

    df.to_csv(path / f'{tsymbol}_prep.csv')


def main():
    tsymbol = sys.argv[1]
    mtdpy, mtd5y = gut.get_min_trading_days()
    path = Path(f'tickers/{tsymbol}')
    df = pd.read_csv(path / f'{tsymbol}_history.csv')
    df_len=len(df)

    prices = df.Close
    prices = df.Close.truncate(before=(df_len-mtd5y)).reset_index().drop('index', axis=1).Close
    prices_len = len(prices)

    gscores = pd.read_csv(path / f'{tsymbol}_micro_gscores.csv', index_col='Unnamed: 0')

    states = np.arange(len(gscores.SH_gScore))
    actions = ['buy', 'hold', 'sell']
    transition_probabilities = np.zeros((len(states), len(states), len(actions)))
    reward_function = np.zeros((len(states), len(actions)))
    for i in range(len(states)):
        for k in range(len(actions)):
            if (k == 'buy'):
                reward_function[i, k] = 0#prices[i+1] - prices[i]
            elif (k == 'sell'):
                reward_function[i, k] = 0#prices[sell_index] - prices[buy_index]
            else:
                reward_function[i, k] = 0

    #Fill in transition probabilities and reward functions
    #mdp = mdp.MDP(states, actions, transition_probabilities, reward_function)


if __name__ == '__main__':
    main()
