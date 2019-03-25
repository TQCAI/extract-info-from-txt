import re

def howManySub(s,sub):
    ans=0
    cnt=0
    l=0
    while ans>=0:
        if ans:
            l=ans+len(sub)
        ans=s.find(sub,l)
        if ans<0:
            break
        cnt+=1
    return cnt



if __name__ == '__main__':
    fname='OUTPUT1.txt'
    with open(fname,'r',encoding='gbk') as f:
        txt=f.read()
    pattern_str=r'\s+?([a-z0-9A-Z_\.]+?)\s*?（需要）'
    pattern=re.compile(pattern_str)
    it=re.finditer(pattern,txt)
    n=0
    for m in it:
        print(m.group(1))
        # try:
        #     print(m.group(2))
        # except :
        #     print('没有这个分组')
        n+=1
    print(f'匹配了{n}个数据')
    print(f'应该匹配{howManySub(txt,"（需要）")}个数据')



