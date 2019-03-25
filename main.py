import re
import pandas as pd

# 键值对
match_keys=['TEMPERATURE',
      'PRESSURE',
      'MOLE FRACTION OF LIQUID L,V'
            ]

# 表格
match_titles=[
    'LIQUID PHASE COMPOSITION',
    'VAPOR PHASE COMPOSITION',
]

output_split_token= '**************PROGRAM RUN OVER***********************'
table_split_token= '*****************************************************'

def process(s):
    '''
    处理table_split_token分隔符， 用于正则表达式匹配
    :param s: 原来的table_split_token
    :return: 转义table_split_token
    '''
    s=s.replace('*',r'\*')
    return s

def gerTableTitle(row):
    '''
    获得列表的表头
    :param row: 列表的第一行
    :return: 表头。list格式
    '''
    # 处理一个bug
    row=row.replace(', ','  ')
    # 把单个空格转化为下划线
    pattern_str=r'\S(\s)\S'
    pattern=re.compile(pattern_str)
    while True:
        ans=pattern.search(row)
        if ans:
            s=ans.start(1)
            e=ans.end(1)
            row=row[:s]+'_'+row[e:]
        else:
            break
    # 用空格分割
    cols=row.split(' ')
    cols = list(filter(lambda x: x, cols))
    # 把下划线转化为空格
    cols=[x.replace('_',' ') for x in cols]
    return cols

def dictDumpToCsv(d,filename='attribute.csv'):
    '''字典存储为csv文件'''
    df=pd.DataFrame(d)
    df.to_csv(filename)



def main():
    '''
    使用说明：
        1. 修改fname为传入的输入文件。需要注意编码格式，默认为gbk
        2. 输出文件默认为'attribute.csv'
    '''
    fname='OUTPUT2.txt'
    with open(fname,'r',encoding='gbk') as f:
        txts=f.read().split(output_split_token)
    output = {}
    for txt in txts:

        # 处理键值对
        pattern_str=r'^(.+):(.+)$'
        pattern=re.compile(pattern_str,re.MULTILINE)
        it=re.finditer(pattern,txt)
        for m in it:
            raw_key=m.group(1)
            raw_value=m.group(2)
            key=raw_key.strip()
            value_list=raw_value.split(' ')
            value_list = list(filter(lambda x: x, value_list))
            value=value_list[0]
            if key in match_keys:
                print(f'{key}\t:\t{value}')
                key=key.replace(' ','_')
                if key in output:
                    output[key].append(value)
                else:
                    output[key]=[]

        # 处理表格
        spliter=process(table_split_token)
        pattern_str = rf'{spliter}(.*?){spliter}'
        pattern=re.compile(pattern_str,re.DOTALL)
        it=re.finditer(pattern,txt)
        for m in it:
            s=m.group(1)
            if len(s)<10:
                continue
            raw_rows=s.split('\n')
            rows=[]
            for row in raw_rows:
                if len(row)>5:
                    rows.append(row)
            titles=gerTableTitle(rows[0])
            items=[]
            wantedIndexs=[]
            wantedTitles=[]
            wantedItems=[]
            for i,title in enumerate(titles):
                if title in match_titles:
                    wantedIndexs.append(i)
                    wantedTitles.append(title)
            for i,row in enumerate(rows[1:]):
                cols = row.split(' ')
                cols = list(filter(lambda x: x, cols))
                items.append(cols)
                wantedItem=[]
                for index in wantedIndexs:
                    value=cols[index]
                    wantedItem.append(value)
                    key=titles[index].replace(' ','_')+f'_{i}'
                    if key in output:
                        output[key].append(value)
                    else:
                        output[key]=[]
                wantedItems.append(wantedItem)
            print(wantedTitles)
            print(wantedItems)
        print(output_split_token)
    print(output)
    dictDumpToCsv(output)


if __name__ == '__main__':
    main()

