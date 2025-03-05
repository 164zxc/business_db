import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Microsoft YaHei'
from datetime import timedelta
import os
st.set_page_config(layout="wide", page_title="商業儀錶板")
def local_css(file_name):
        with open(
            "./style.css", "r", encoding="utf-8"
        ) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")
# 設定選擇日期
#預設日期
select_date1 = datetime(2024, 10,1)
select_date2 = datetime(2024, 10,30)

min_date = datetime(2020, 1, 1)
max_date = datetime(datetime.today().year, 12, 31)

# #連結數據庫
# Username = "TKB5329_Course_Sale"
# Password = Config.business_password
# host = Config.business_host
# port = Config.business_port
# database = "course_sale_data"
# engine = create_engine(f'mysql+pymysql://{Username}:{Password}@{host}:{port}/{database}')

current_folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_folder, "area_data.csv")

def setting_data(select_date1, select_date2):
    
    #將日期轉為字串才能進行SQL搜尋
    select_date_str1 = select_date1.strftime('%Y-%m-%d')
    select_date_str2 = select_date2.strftime('%Y-%m-%d')
    
    select_date_pre_str1 = (select_date1 - timedelta(days=365)).strftime('%Y-%m-%d')
    select_date_pre_str2 = (select_date2 - timedelta(days=365)).strftime('%Y-%m-%d')
    
    df = pd.read_csv('ftable.csv')
    df_select = df[(df['CREATE_DATE']>=select_date_str1)&(df['CREATE_DATE']<=select_date_str2)]
    df_select_pre = df[(df['CREATE_DATE']>=select_date_pre_str1)&(df['CREATE_DATE']<=select_date_pre_str2)]
    
    # query = f"SELECT * FROM MERGED_DATA WHERE CREATE_DATE BETWEEN '{select_date_str1}' AND '{select_date_str2}'"
    # df_select = pd.read_sql(query, con=engine)
    
    # query = f"SELECT * FROM MERGED_DATA WHERE CREATE_DATE BETWEEN '{select_date_pre_str1}' AND '{select_date_pre_str2}'"
    # df_select_pre = pd.read_sql(query, con=engine)
    
    
    if '區域' in df_select.columns:
        pass
    # 判斷檔案是否存在
    elif os.path.exists(file_path):
        new_data = pd.read_csv(file_path)
        df_select = pd.merge(df_select,new_data,on='LOCATION',how='left')
        df_select = df_select.fillna('未知')
        df_select_pre = pd.merge(df_select_pre,new_data,on='LOCATION',how='left')
        df_select_pre = df_select_pre.fillna('未知')
    else:
        df_select['區域']='未知'
        df_select_pre['區域']='未知'
                        
    return df_select,df_select_pre

#建立進階搜尋選項
def option_data(option_region,option_shop,option_category,option_sub_category,option_teacher,option_exam,df,df_pre):
        
    if option_region==[]:
        pass
    else:
        df = df[df['區域'].isin(list(option_region))]
        df_pre = df_pre[df_pre['區域'].isin(list(option_region))]
    
    if option_shop==[]:
        pass
    else:
        df = df[df['LOCATION'].isin(list(option_shop))]
        df_pre = df_pre[df_pre['LOCATION'].isin(list(option_shop))]
        
    if option_category==[]:
        pass
    else:
        df = df[df['COURSE_TYPE_SUB'].isin(list(option_category))]
        df_pre = df_pre[df_pre['COURSE_TYPE_SUB'].isin(list(option_category))] 
        
    if option_sub_category==[]:
        pass
    else:
        df = df[df['SUBJECT_NAME'].isin(list(option_sub_category))]
        df_pre = df_pre[df_pre['SUBJECT_NAME'].isin(list(option_sub_category))]
        
    if option_teacher==[]:
        pass
    else:
        df = df[df['TEACHER'].isin(list(option_teacher))]
        df_pre = df_pre[df_pre['TEACHER'].isin(list(option_teacher))]
    
    if option_exam==[]:
        pass
    else:
        df = df[df['EXAM_TYPE'].isin(list(option_exam))]
        df_pre = df_pre[df_pre['EXAM_TYPE'].isin(list(option_exam))]
            
    # place = (','.join(df_option['區域'].unique().astype(str)))
    # shop = (','.join(df_option['LOCATION'].unique().astype(str)))
    # category = (','.join(df_option['COURSE_TYPE_SUB'].unique().astype(str)))
    # sub_category = (','.join(df_option['SUBJECT_NAME'].unique().astype(str)))
    # teacher = (','.join(df_option['TEACHER'].unique().astype(str)))
    # exam = (','.join(df_option['EXAM_TYPE'].unique().astype(str)))
    
    # if len(df_option['區域'].unique())==1:
    #     df = df[df['區域']==place]
    #     df_pre = df_pre[df_pre['區域']==place]
    # else:
    #     pass
    # if len(df_option['LOCATION'].unique())==1:
    #     df = df[df['LOCATION']==shop]
    #     df_pre = df_pre[df_pre['LOCATION']==shop]
    # else:
    #     pass
    # if len(df_option['COURSE_TYPE_SUB'].unique())==1:
    #     df = df[df['COURSE_TYPE_SUB']==category]
    #     df_pre = df_pre[df_pre['COURSE_TYPE_SUB']==category]
    # else:
    #     pass
    # if len(df_option['SUBJECT_NAME'].unique())==1:
    #     df = df[df['SUBJECT_NAME']==sub_category]
    #     df_pre = df_pre[df_pre['SUBJECT_NAME']==sub_category]
    # else:
    #     pass
    # if len(df_option['TEACHER'].unique())==1:
    #     df = df[df['TEACHER']==teacher]
    #     df_pre = df_pre[df_pre['TEACHER']==teacher]
    # else:
    #     pass
    # if len(df_option['EXAM_TYPE'].unique())==1:
    #     df = df[df['EXAM_TYPE']==exam]
    #     df_pre = df_pre[df_pre['EXAM_TYPE']==exam]
    # else:
    #     pass
    
    return df,df_pre
    

#建立數字格式(千分位、縮寫)
def shorten_number(value):
    if value >= 1_000_000:  # 百萬
        return f"{value / 1_000_000:.2f}M"  # 顯示到小數點後兩位
    elif value >= 1_000:  # 千
        return f"{value / 1_000:.2f}K"
    else:
        return f"{int(value)}"
        
# 自定義文本標籤：顯示當前值和變化值
@st.cache_data
def format_text(row):
    
    change = row['CHANGE']
    compare = row['COMPARE']
    
    #當數據對比不同狀況時顯示不同格式
    if change > 0:
        color = "green"  # 上升的字體顏色
    elif change < 0:
        color = "red"    # 下降的字體顏色
    else:
        color = "gray"   # 無變化的字體顏色
        
    cur_value = shorten_number(row['ORDER_PRICE_CUR'])
                        
    if compare > 0:
        return f"<b>{cur_value}</b><br><span style='color:{color};'>(+{change}%)</span>" 
    elif compare < 0:
        return f"<b>{cur_value}</b><br><span style='color:{color};'>({change}%)</span>"  
    else:
        return f"<b>{cur_value}</b><br>(0.00%)"    
#自訂圖表樣式
def plot_format():
    fig.update_layout(
        xaxis_title='',
        yaxis_visible=False, 
        title_font_size=20,
        margin=dict(l=10, r=10, t=80, b=30),
        shapes=[
            # 在圖表中添加一條 y=0 的直線
            {
                'type': 'line',
                'x0': 0,  # 起始位置 (x 軸)
                'y0': 0,  # 起始位置 (y 軸)
                'x1': 1,  # 結束位置 
                'y1': 0,  # 結束位置 
                'xref': 'paper',  # 使用整個圖形的範圍
                'yref': 'paper',  # 使用整個圖形的範圍
                'line': {
                    'color': 'gray',  # 直線顏色
                    'width': 1         # 直線寬度
                }
            }
        ],
    )

    # 更新數值標籤的位置和角度
    fig.update_traces(
        textangle=0, 
        textposition="outside",
        texttemplate='%{text}',  # 確保自定義文本正確顯示
    )

    # 顯示圖表
    st.plotly_chart(fig, use_container_width=True)       
############################################################################################################################################
############################################################## 開始進行儀表板製作 ############################################################
############################################################################################################################################

col1,col2,col3,col4 = st.columns([2,1.5,1,0.4])
with col1:
    st.title('營運報表')
    
with col3:
    
    #日期選擇工具
    date_input = st.date_input(
        "",(select_date1,select_date2),
        min_date,
        max_date,
        format="YYYY.MM.DD",
    )
    #避免只選擇單個日期的狀況
    if isinstance(date_input, tuple) and len(date_input) == 2:
        select_date1, select_date2 = date_input  # 日期範圍
        
with col4:
    # st.write(f'最後更新日期 : {datetime.today().date()}')  
    st.write('######')
    #呼叫讀取數據  
    df_select,df_select_pre = setting_data(select_date1,select_date2)  
    
    #建立進階選擇器

    with st.popover("進階篩選"):
        
        
        @st.fragment
        def my_fragment_setting():
            df_option = df_select.copy()
                
            option_region = st.multiselect('選擇地區',list(df_option['區域'].unique()),placeholder='所有區域')
            if option_region !=[]:
                df_option = df_option[df_option['區域'].isin(option_region)]
                    
            option_shop = st.multiselect('選擇分店',list(df_option['LOCATION'].unique()),placeholder='所有分店')
            if option_shop!=[]:
                df_option = df_option[df_option['LOCATION'].isin(option_shop)]
                
            option_category = st.multiselect('選擇類別',list(df_option['COURSE_TYPE_SUB'].unique()),placeholder='所有產品類別')
            if option_category!=[]:
                df_option = df_option[df_option['COURSE_TYPE_SUB'].isin(option_category)]
                
            option_sub_category = st.multiselect('選擇子類別',list(df_option['SUBJECT_NAME'].unique()),placeholder='所有產品子類別')
            if option_sub_category!=[]:
                df_option = df_option[df_option['SUBJECT_NAME'].isin(option_sub_category)]
                
            option_teacher = st.multiselect('選擇老師',list(df_option['TEACHER'].unique()),placeholder='所有老師')
            if option_teacher!=[]:
                df_option = df_option[df_option['TEACHER'].isin(option_teacher)]
                
            option_exam = st.multiselect('選擇考試類別',list(df_option['EXAM_TYPE'].unique()),placeholder='所有考試類別')
            if option_exam!=[]:
                df_option = df_option[df_option['EXAM_TYPE'].isin(option_exam)]
            
            return option_region,option_shop,option_category,option_sub_category,option_teacher,option_exam
        option_region,option_shop,option_category,option_sub_category,option_teacher,option_exam = my_fragment_setting()
        
        if st.button('開始篩選',use_container_width=True):
            df,df_pre = option_data(option_region,option_shop,option_category,option_sub_category,option_teacher,option_exam,df_select,df_select_pre)
        else:
            df,df_pre = df_select,df_select_pre
        
#設定目標值(去年同期*1.1)
goal = (df_pre.groupby('STUDENT_NO_DETAIL_ITEM')[['ORDER_TOTAL','DISCOUNT_AMOUNT']].max().reset_index()[['ORDER_TOTAL','DISCOUNT_AMOUNT']].sum().sum())*1.1

#建立數據檢視選擇器


        
tab1,tab2,tab3,tab4,tab5 = st.tabs(['營業數據','產品數據','客戶數據','員工表現','區域設定'])

#建立重要指標可視區

with tab1:
    
    col1,col2,col3,col4,col5 = st.columns(5)
    
    dplot = df.loc[df.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
    dplot['營業額'] = dplot['ORDER_TOTAL']+dplot['DISCOUNT_AMOUNT']
    dplot_pre = df_pre.loc[df_pre.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
    dplot_pre['營業額'] = dplot_pre['ORDER_TOTAL']+dplot_pre['DISCOUNT_AMOUNT']
    
    with col1:
        current_value = round(dplot['營業額'].sum())
        previous_value = round(dplot_pre['營業額'].sum())
        delta_value = current_value - previous_value
        if previous_value != 0:
            growth_rate = (delta_value / previous_value) * 100
        else:
            growth_rate = 0 
            
        # 格式化數字(添加逗號分隔)
        formatted_value = f"{current_value:,}"  
        formatted_delta = f"{growth_rate:.2f}% "    

        # 使用 st.metric 顯示格式化數據
        st.metric(
            label="營業額", 
            value=formatted_value, 
            delta=formatted_delta
        )
    with col2:
        current_value = round(dplot['ORDER_TOTAL'].sum())
        previous_value = round(dplot_pre['ORDER_TOTAL'].sum())
        delta_value = current_value - previous_value
        if previous_value != 0:
            growth_rate = (delta_value / previous_value) * 100
        else:
            growth_rate = 0 
        formatted_value = f"{current_value:,}"  
        formatted_delta = f"{growth_rate:.2f}%"  

        st.metric(
            label="商家實收", 
            value=formatted_value, 
            delta=formatted_delta
        )
    with col3:
        current_value = round(dplot['DISCOUNT_AMOUNT'].sum())
        previous_value = round(dplot_pre['DISCOUNT_AMOUNT'].sum())
        delta_value = current_value - previous_value
        if previous_value != 0:
            growth_rate = (delta_value / previous_value) * 100
        else:
            growth_rate = 0 
            
        formatted_value = f"{current_value:,}"  
        formatted_delta = f"{growth_rate:.2f}% "   

        st.metric(
            label="商家補貼", 
            value=formatted_value, 
            delta=formatted_delta
        )
    with col4:
        current_value = round(dplot['INVOICE_NO'].nunique())
        previous_value = round(dplot_pre['INVOICE_NO'].nunique())
        delta_value = current_value - previous_value
        if previous_value != 0:
            growth_rate = (delta_value / previous_value) * 100
        else:
            growth_rate = 0 
            
        formatted_value = f"{current_value:,}" 
        formatted_delta = f"{growth_rate:.2f}% " 
        
        st.metric(
            label="訂單總數", 
            value=formatted_value, 
            delta=formatted_delta
        )
        
    with col5:
        current_value = round(dplot['ORDER_TOTAL'].sum() / dplot['INVOICE_NO'].nunique())
        previous_value = round(dplot_pre['ORDER_TOTAL'].sum() / dplot_pre['INVOICE_NO'].nunique())
        delta_value = current_value - previous_value
        if previous_value != 0:
            growth_rate = (delta_value / previous_value) * 100
        else:
            growth_rate = 0 
            
        # 格式化數字
        formatted_value = f"{current_value:,}"  # 添加逗號分隔
        formatted_delta = f"{growth_rate:.2f}%" 
        # 使用 st.metric 顯示格式化數據
        st.metric(
            label="客單價", 
            value=formatted_value, 
            delta=formatted_delta
        )
    with st.container():
        fig = go.Figure(go.Indicator(
            mode="gauge", 
            value=dplot['營業額'].sum(), 
            gauge={
                'shape': "bullet",  # 設置儀表形狀為"bullet"
                'axis': {'range': [None, goal]},  # 設定儀表範圍
                'bar': {'color': "rgb(161, 128, 255)"},  # 設定背景顏色
            },
            domain={'x': [0, 1], 'y': [0, 0.5]},# 設定儀表圖在畫布上的位置
            
        ))
        fig.update_layout(
                        margin=dict(l=0, r=0, t=0, b=30),
                        height=50,       
                        paper_bgcolor='#f4f7fc', #畫布底色
                        plot_bgcolor='#f4f7fc',
                    )
        fig.add_annotation(
            x=1,  
            y=1.3,
            text="GOAL",
            showarrow=False,  # 不顯示箭頭
        )
        
        st.plotly_chart(fig,use_container_width=True)
    
    data = df.loc[df.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
    
    col1,col2 = st.columns([1,0.6])
    with col1:
        dplot = pd.pivot_table(data=data,index='CREATE_DATE',values=['ORDER_TOTAL','DISCOUNT_AMOUNT'],aggfunc='sum').reset_index()
        dplot['營業額'] = dplot['ORDER_TOTAL']+dplot['DISCOUNT_AMOUNT']

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dplot['CREATE_DATE'],
            y=dplot['營業額'],
            line=dict(color="rgb(161, 128, 255)"),
            name='營業額',
            hovertemplate='<b>Date:</b> %{x}<br>' +  # 日期
                        '<b>營業額:</b> %{y}<br>'   # 訂單金額
        ))
        fig.add_trace(go.Scatter(
            x=dplot['CREATE_DATE'],
            y=dplot['ORDER_TOTAL'],
            line=dict(color='rgb(57, 52 ,186)', width=2),
            name='商家實收',
            hovertemplate='<b>Date:</b> %{x}<br>' +  # 日期
                        '<b>商家實收:</b> %{y}<br>'   # 訂單金額
        ))
        fig.add_trace(go.Scatter(
            x=dplot['CREATE_DATE'],
            y=dplot['DISCOUNT_AMOUNT'],
            line=dict(color='skyblue'),
            name='商家補貼',
            hovertemplate='<b>Date:</b> %{x}<br>' +  # 日期
                        '<b>商家補貼:</b> %{y}<br>'   # 訂單金額
        ))
        fig.update_layout(
                            title=f" 營業概況",
                            title_font_size=20,
                            xaxis=dict(title="", tickformat="%m-%d\n%Y"),
                            yaxis=dict(range=[0, dplot['營業額'].max() * 1.2]),
                            margin=dict(l=10, r=10, t=80, b=30),
                            legend=dict(x=0.7, y=1.1, orientation='h',font=dict(size=16)),
                            
                        )
        
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
        data['CREATE_DATE'] = pd.to_datetime(data['CREATE_DATE'])
        data['dayofweek'] = data['CREATE_DATE'].dt.dayofweek
        full_week = pd.DataFrame({'dayofweek': range(7)})
        dplot = pd.pivot_table(data=data,index='dayofweek',values='ORDER_TOTAL',aggfunc='sum')
        dplot = full_week.merge(dplot, on='dayofweek', how='left').fillna(0)  # 補全缺失天數，空值填 0
        dplot['dayofweek']=["週一","週二","週三","週四","週五","週六","週日"]
        
        dplot.columns=['dayofweek','商家實收']
        dplot = dplot.reset_index()
        fig = px.bar(dplot,x='dayofweek',y='商家實收',hover_data={'dayofweek':True,'商家實收':':,'},labels={'dayofweek':'星期'})
        fig.update_layout(
                            title=f" 每日實收",
                            title_font_size=20,
                            xaxis=dict(title="", tickformat="%m-%d\n%Y"),
                            yaxis=dict(title='',range=[0, dplot['商家實收'].max() * 1.2]),
                            margin=dict(l=10, r=10, t=80, b=30),
                        )
        fig.update_traces(
            #更改柱狀圖顏色
            marker_color = 'rgb(57, 52 ,186)'
        )
        st.plotly_chart(fig,use_container_width=True)

    with st.container():        
        dplot = pd.pivot_table(data=data,index='CREATE_DATE',values=['ORDER_TOTAL','INVOICE_NO'],aggfunc={'ORDER_TOTAL':'sum','INVOICE_NO':'nunique'}).reset_index()
        dplot.columns = ['CREATE_DATE','ORDER','商家實收']
        dplot['客單價'] = round(dplot['商家實收']/dplot['ORDER']).astype(int)
        
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=dplot['CREATE_DATE'], 
            y=dplot['ORDER'], 
            name='訂單數',  # 折線名稱
            marker=dict(
                color='skyblue',  # 長條顏色
            ),
            hovertemplate='<b>Date:</b> %{x}<br>' +  # 日期
                        '<b>訂單數:</b> %{y}<br>'   # 訂單金額
                    # 指定次 Y 軸
        ))
        fig.add_trace(go.Scatter(
            x=dplot['CREATE_DATE'],  # X 軸
            y=dplot['客單價'],
            mode='lines+markers',
            name='客單價',  # 折線名稱
            line=dict(color='rgb(57, 52 ,186)'),
            yaxis='y2', # 增加線條寬度
            hovertemplate='<b>Date:</b> %{x}<br>' +  # 日期
                        '<b>客單價:</b> %{y:,}<br>'   # 訂單金額
        ))



        # 更新圖表布局以支持雙軸
        fig.update_layout(
            title=" 訂單總數與客單價概況",
            title_font_size=20,
            xaxis=dict(title="", tickformat="%m-%d\n%Y"),  # 設置 X 軸格式
            yaxis=dict(
                title="訂單數",  # 次 Y 軸標題
                range=[0, dplot['ORDER'].max() * 1.2]
            ),
            yaxis2=dict(
                title="客單價",  # 主 Y 軸標題
                overlaying='y',  # 次 Y 軸與主 Y 軸疊加
                side='right',  # 次 Y 軸顯示在右側
                range=[0, dplot['客單價'].max() * 1.2],
                showline=False,
                showgrid=False
            ),
            margin=dict(l=10, r=10, t=80, b=30),
            legend=dict(x=0.84, y=1.1, orientation='h',font=dict(size=16)),  # 調整圖例位置
        )
        st.plotly_chart(fig,use_container_width=True)

        # 計算當前年數據
        if '區域' in df.columns:
            dplot = df.loc[df.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
            dplot = dplot.groupby('區域')['ORDER_TOTAL'].sum().reset_index()
            dplot_pre = df_pre.loc[df_pre.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
            dplot_pre = dplot_pre.groupby('區域')['ORDER_TOTAL'].sum().reset_index()
    
            dplot.columns = ['區域', 'ORDER_PRICE_CUR']
            dplot_pre.columns = ['區域', 'ORDER_PRICE_PREV']

            # 合併當前年和去年的數據，並計算變化值
            combined = pd.merge(dplot, dplot_pre, on='區域', how='outer').fillna(0)
            combined['CHANGE'] = round((combined['ORDER_PRICE_CUR'] - combined['ORDER_PRICE_PREV']) / combined['ORDER_PRICE_PREV'] * 100, 2)
            combined['COMPARE'] = combined['ORDER_PRICE_CUR']-combined['ORDER_PRICE_PREV']

            combined = combined.sort_values('ORDER_PRICE_CUR', ascending=False).head(10)
            combined['TEXT'] = combined.apply(format_text, axis=1)

            # 繪製條形圖
         
            fig = px.bar(combined, 
                        x='區域', 
                        y='ORDER_PRICE_CUR', 
                        text='TEXT',
                        labels={'TEXT':'商家實收'},
                        hover_data={'ORDER_PRICE_CUR':False}
            )


            # 更新圖表樣式
            fig.update_layout(
                title=f" 各區業績表現",
                yaxis=dict(range=[0, combined['ORDER_PRICE_CUR'].max() * 1.2]),
            )
            fig.update_traces(
                marker_color = 'rgb(141 ,211 ,199)'
            )
            
            plot_format()
        
with tab2: 
#建立業績目標進度條
    col1,col2 = st.columns([1,0.15])
    with col2:
        options = ['商家實收','銷售數量']
        selection = st.segmented_control(
            "", options, selection_mode="single", default='商家實收'
        )
        if selection == '商家實收':
            title_head = '商家實收'
        else:
            title_head = '銷售數量'             
            
    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        
        
        #地區數據
        
        dplot = df.loc[df.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
        dplot_pre = df_pre.loc[df_pre.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
        if selection == '商家實收':
            dplot = dplot.groupby('LOCATION')['ORDER_TOTAL'].sum().reset_index().sort_values('ORDER_TOTAL')
            dplot_pre = dplot_pre.groupby('LOCATION')['ORDER_TOTAL'].sum().reset_index().sort_values('ORDER_TOTAL')
        else:
            dplot = dplot.groupby('LOCATION')['ORDER_TOTAL'].count().reset_index().sort_values('ORDER_TOTAL')
            dplot_pre = dplot_pre.groupby('LOCATION')['ORDER_TOTAL'].count().reset_index().sort_values('ORDER_TOTAL')
        
        dplot.columns = ['分館', 'ORDER_PRICE_CUR']
        dplot_pre.columns = ['分館', 'ORDER_PRICE_PREV']
            
        # 合併當前年和去年的數據，並計算變化值
        combined = pd.merge(dplot, dplot_pre, on='分館', how='outer').fillna(0)
        combined['CHANGE'] = round((combined['ORDER_PRICE_CUR'] - combined['ORDER_PRICE_PREV']) / combined['ORDER_PRICE_PREV'] * 100, 2)
        combined['COMPARE'] = combined['ORDER_PRICE_CUR']-combined['ORDER_PRICE_PREV']

        combined = combined.sort_values('ORDER_PRICE_CUR')
        combined['TEXT'] = combined.apply(format_text, axis=1)
                    
        fig = px.bar(combined,x='ORDER_PRICE_CUR',y='分館',orientation='h', text='TEXT',
                        hover_data={'TEXT':False},labels={'ORDER_PRICE_CUR':title_head},
                        
                    )
        fig.update_layout(
            title=f" {title_head} | 分館",
            xaxis_title='',
            xaxis=dict(range=[0, combined['ORDER_PRICE_CUR'].max() * 1.2]),
            yaxis_title='',
            title_font_size=20 ,
            height=915,
        )
        fig.update_traces(
            marker_color='rgb(57, 52 ,186)',
            textposition="outside",
            texttemplate='%{text}'
            )
        st.plotly_chart(fig,use_container_width=True)
        
        
    with col2:
        
        # 計算當前年數據
        
        if selection == '商家實收':
            dplot = df.groupby('COURSE_TYPE_SUB')[['ORDER_PRICE']].sum().reset_index()
            dplot_pre = df_pre.groupby('COURSE_TYPE_SUB')[['ORDER_PRICE']].sum().reset_index()
        else:
            dplot = df.groupby('COURSE_TYPE_SUB')[['ORDER_PRICE']].count().reset_index()
            dplot_pre = df_pre.groupby('COURSE_TYPE_SUB')[['ORDER_PRICE']].count().reset_index()
            
        dplot.columns = ['COURSE_TYPE_SUB', 'ORDER_PRICE_CUR']
        dplot_pre.columns = ['COURSE_TYPE_SUB', 'ORDER_PRICE_PREV']

        # 合併當前年和去年的數據，並計算變化值
        combined = pd.merge(dplot, dplot_pre, on='COURSE_TYPE_SUB', how='outer').fillna(0)
        combined['CHANGE'] = round((combined['ORDER_PRICE_CUR'] - combined['ORDER_PRICE_PREV']) / combined['ORDER_PRICE_PREV'] * 100, 2)
        combined['COMPARE'] = combined['ORDER_PRICE_CUR']-combined['ORDER_PRICE_PREV']

        combined = combined.sort_values('ORDER_PRICE_CUR', ascending=False)
        combined['TEXT'] = combined.apply(format_text, axis=1)

        # 繪製條形圖(默認顯示前5行數據)
        fig = px.bar(combined.head(5),
                    x='COURSE_TYPE_SUB',
                    y='ORDER_PRICE_CUR', 
                    text='TEXT',  # 使用自定義文本標籤
                    hover_data={'ORDER_PRICE_CUR':False},
                    labels={'TEXT': title_head, 'COURSE_TYPE_SUB': 'Course Type'})
        #建立圖內篩選
        updatemenus = [
        {
            "buttons": [
                
                {
                    "label": "Top 5",
                    "method": "update",
                    "args": [
                        {"x": [combined['COURSE_TYPE_SUB'][:5]], "y": [combined['ORDER_PRICE_CUR'][:5]], "text": [combined['TEXT'][:5]]}
                    ]
                },
                {
                    "label": "All",
                    "method": "update",
                    "args": [
                        {"x": [combined['COURSE_TYPE_SUB']], "y": [combined['ORDER_PRICE_CUR']], "text": [combined['TEXT']]}
                    ]
                }
                
            ],
            "direction": "down",  # 下拉選單
            "showactive": True,   # 高亮當前選擇
            "x": 1.1,             # 設定 X 軸位置 (1.0 是圖表右邊界)
            "y": 1.2              # 設定 Y 軸位置 (1.0 是圖表上邊界)
        }
    ]

        # 更新圖表樣式
        fig.update_layout(
            title=f" {title_head} | 產品類別",
            updatemenus=updatemenus,
            bargap=0.5,
            yaxis=dict(range=[0, combined['ORDER_PRICE_CUR'].max() * 1.2]),
        )
        fig.update_traces(
            #更改柱狀圖顏色
            marker_color = 'rgb(57, 52 ,186)'
        )
        plot_format()
                    
        # 計算當前年數據
        if selection == '商家實收':
            dplot = df.groupby('SUBJECT_NAME')[['ORDER_PRICE']].sum().reset_index()
            dplot_pre = df_pre.groupby('SUBJECT_NAME')[['ORDER_PRICE']].sum().reset_index()
        else:
            dplot = df.groupby('SUBJECT_NAME')[['ORDER_PRICE']].count().reset_index()
            dplot_pre = df_pre.groupby('SUBJECT_NAME')[['ORDER_PRICE']].count().reset_index()
            
        dplot.columns = ['SUBJECT_NAME', 'ORDER_PRICE_CUR']
        dplot_pre.columns = ['SUBJECT_NAME', 'ORDER_PRICE_PREV']

        # 合併當前年和去年的數據，並計算變化值
        combined = pd.merge(dplot, dplot_pre, on='SUBJECT_NAME', how='outer').fillna(0)
        combined['CHANGE'] = round((combined['ORDER_PRICE_CUR'] - combined['ORDER_PRICE_PREV']) / combined['ORDER_PRICE_PREV'] * 100, 2)
        combined['COMPARE'] = combined['ORDER_PRICE_CUR']-combined['ORDER_PRICE_PREV']

        combined = combined.sort_values('ORDER_PRICE_CUR', ascending=False).head(10)
        combined['TEXT'] = combined.apply(format_text, axis=1)

        # 繪製條形圖
        fig = px.bar(combined, 
                    x='SUBJECT_NAME', 
                    y='ORDER_PRICE_CUR', 
                    text='TEXT',  # 使用自定義文本標籤
                    hover_data={'ORDER_PRICE_CUR':False},
                    labels={'TEXT': title_head, 'SUBJECT_NAME': '科目'})

        # 更新圖表樣式
        fig.update_layout(
            title=f" {title_head} | 產品子類別",
            yaxis=dict(range=[0, combined['ORDER_PRICE_CUR'].max() * 1.2]),
        )
        fig.update_traces(
            marker_color = 'skyblue'
        )
        
        plot_format()
                
    with col3:
        
        # 計算當前年數據
        if selection == '商家實收':
            dplot = df.groupby('TEACHER')[['ORDER_PRICE']].sum().reset_index()
        else:
            dplot = df.groupby('TEACHER')[['ORDER_PRICE']].count().reset_index()
        
        dplot.columns = ['TEACHER', 'ORDER_PRICE_CUR']

        # 計算前一年數據
        if selection == '商家實收':
            dplot_pre = df_pre.groupby('TEACHER')[['ORDER_PRICE']].sum().reset_index()
        else:
            dplot_pre = df_pre.groupby('TEACHER')[['ORDER_PRICE']].count().reset_index()
            
        dplot_pre.columns = ['TEACHER', 'ORDER_PRICE_PREV']

        # 合併當前年和去年的數據，並計算變化值
        combined = pd.merge(dplot, dplot_pre, on='TEACHER', how='outer').fillna(0)
        combined['CHANGE'] = round((combined['ORDER_PRICE_CUR'] - combined['ORDER_PRICE_PREV']) / combined['ORDER_PRICE_PREV'] * 100, 2)
        combined['COMPARE'] = combined['ORDER_PRICE_CUR']-combined['ORDER_PRICE_PREV']

        combined = combined.sort_values('ORDER_PRICE_CUR', ascending=False)
        combined['TEXT'] = combined.apply(format_text, axis=1)
        # 繪製條形圖
        fig = px.bar(combined.head(5), 
                    x='TEACHER', 
                    y='ORDER_PRICE_CUR', 
                    text='TEXT',  # 使用自定義文本標籤
                    hover_data={'ORDER_PRICE_CUR':False},
                    labels={'TEXT': title_head, })

        updatemenus = [
            {
                "buttons": [
                    
                    {
                        "label": "Top 5",
                        "method": "update",
                        "args": [
                            {"x": [combined['TEACHER'][:5]], "y": [combined['ORDER_PRICE_CUR'][:5]], "text": [combined['TEXT'][:5]]}
                        ]
                    },
                    {
                        "label": "All",
                        "method": "update",
                        "args": [
                            {"x": [combined['TEACHER']], "y": [combined['ORDER_PRICE_CUR']], "text": [combined['TEXT']]}
                        ]
                    }
                    
                ],
                "direction": "down",  # 下拉選單
                "showactive": True,   # 高亮當前選擇
                "x": 1.1,             # 設定 X 軸位置 (1.0 是圖表右邊界)
                "y": 1.2              # 設定 Y 軸位置 (1.0 是圖表上邊界)
            }
        ]
        # 更新圖表樣式
        fig.update_layout(
            title=f" {title_head} | 講課老師",
            yaxis=dict(range=[0, combined['ORDER_PRICE_CUR'].max() * 1.2]),
            bargap=0.5,
            updatemenus=updatemenus,
        )
        fig.update_traces(
            marker_color = 'rgb(141 ,211 ,199)'
        )
        plot_format()
        
        
        # 計算當前年數據
        if selection == '商家實收':
            dplot = df.groupby('PROGRAM_TYPE')[['ORDER_PRICE']].sum().reset_index()
            dplot_pre = df_pre.groupby('PROGRAM_TYPE')[['ORDER_PRICE']].sum().reset_index()
        else:
            dplot = df.groupby('PROGRAM_TYPE')[['ORDER_PRICE']].count().reset_index()
            dplot_pre = df_pre.groupby('PROGRAM_TYPE')[['ORDER_PRICE']].count().reset_index()
        
        dplot.columns = ['PROGRAM_TYPE', 'ORDER_PRICE_CUR']
        dplot_pre.columns = ['PROGRAM_TYPE', 'ORDER_PRICE_PREV']

        # 合併當前年和去年的數據，並計算變化值
        combined = pd.merge(dplot, dplot_pre, on='PROGRAM_TYPE', how='outer').fillna(0)
        combined['CHANGE'] = round((combined['ORDER_PRICE_CUR'] - combined['ORDER_PRICE_PREV']) / combined['ORDER_PRICE_PREV'] * 100, 2)
        combined['COMPARE'] = combined['ORDER_PRICE_CUR']-combined['ORDER_PRICE_PREV']

        combined = combined.sort_values('ORDER_PRICE_CUR', ascending=False).head(10)
        combined['TEXT'] = combined.apply(format_text, axis=1)

        # 繪製條形圖
        fig = px.bar(combined, 
                    x='PROGRAM_TYPE', 
                    y='ORDER_PRICE_CUR', 
                    text='TEXT',  # 使用自定義文本標籤
                    hover_data={'ORDER_PRICE_CUR':False},
                    labels={'TEXT': title_head,'PROGRAM_TYPE': 'Exam' })
                    

        # 更新圖表樣式
        fig.update_layout(
            title=f" {title_head} | 考試類別",
            yaxis=dict(range=[0, combined['ORDER_PRICE_CUR'].max() * 1.2]),
        )
        fig.update_traces(
            marker_color =' rgb(251, 128 ,114)'
        )
        plot_format()
        
with tab3:    
    col1,col2,col3 = st.columns([1,1,0.6])
    with col1:   
        
        dplot = df.loc[df.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
        dplot = dplot.groupby(['SEXUAL','PROGRAM_TYPE'])['STUDENT_NO_DETAIL_ITEM'].count().reset_index().sort_values('STUDENT_NO_DETAIL_ITEM',ascending=False)
        dplot = dplot[dplot['PROGRAM_TYPE'].isin(list(dplot['PROGRAM_TYPE'].head(10)))]
        dplot.rename(columns={'SEXUAL':'性別'},inplace=True)
        dplot['性別'].replace({'Male':'男','Female':'女'},inplace=True)
        
        fig = px.bar(dplot,x='PROGRAM_TYPE',y='STUDENT_NO_DETAIL_ITEM',
                        color='性別',barmode='group'
                        ,color_discrete_map={  # 指定顏色映射
                            '男': 'rgb(0 ,104, 201)',
                            '女': 'rgb(131, 201 ,255)'
                        },labels={'PROGRAM_TYPE': '科目類別','STUDENT_NO_DETAIL_ITEM': '銷售數量' })
        
        fig.update_layout(
                            title=f" 產品 | 性別對比",
                            title_font_size=20,
                            xaxis=dict(title=""),
                            yaxis=dict(title='銷售數量',range=[0, dplot['STUDENT_NO_DETAIL_ITEM'].max() * 1.2]),
                            margin=dict(l=10, r=10, t=80, b=10),
                            legend=dict(x=0.8, y=1.1, orientation='h'),
                        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        
        pivot_table = pd.pivot_table(data=dplot,index='性別',columns='PROGRAM_TYPE',aggfunc='sum',values='STUDENT_NO_DETAIL_ITEM')
        pivot_table = (pivot_table/pivot_table.sum())    
        pivot_table = pivot_table.T[['男','女']]
        
        fig = px.bar(pivot_table,orientation='h',text_auto='.0%',labels={'PROGRAM_TYPE': '科目類別'},
                     color_discrete_map={  # 指定顏色映射
                            '男': 'rgb(0 ,104, 201)',
                            '女': 'rgb(131, 201 ,255)'
                        },hover_data={'value':False})
        fig.update_layout(
                            title=f" 產品 | 性別占比",
                            title_font_size=20,
                            xaxis_visible = False,
                            yaxis=dict(title=''),
                            margin=dict(l=10, r=20, t=60, b=30),
                            legend_visible = False,
                        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col3:
        dplot = df.groupby('STUDENT_NO')['SEXUAL'].max().reset_index()
        dplot = dplot['SEXUAL'].value_counts().reset_index()
        dplot['SEXUAL'].replace({'Female':'女','Male':'男'},inplace=True)
        fig = px.pie(dplot,values='count',names='SEXUAL',hole=.5,
                        color_discrete_map={  # 指定顏色映射
                            '男': 'rgb(0 ,104, 201)',
                            '女': 'rgb(131, 201 ,255)'
                        },
                        labels={'SEXUAL': '性別','count': '人數' }
                        )
        fig.update_traces(
                textinfo="percent+label",  # 顯示標籤和數值
                textposition='inside'  # 設置文字大小
            )
        fig.update_layout(
            title=' 客戶男女比例',
            title_font_size=20,
            showlegend=False,
            margin=dict(l=10, r=10, t=80, b=30),
        )
        st.plotly_chart(fig,use_container_width=True)
            
    col1,col2,col3 = st.columns([1,0.6,1])
    with col1:
        
        dplot = df[df['AGE']!='Missing']
        dplot = dplot.groupby('STUDENT_NO')[['AGE','SEXUAL']].max().reset_index()
        dplot['SEXUAL'].replace({'Male':'男','Female':'女'},inplace=True)
        #原數據的年齡有小數
        dplot['AGE'] = dplot['AGE'].astype(float)
        dplot['AGE'] = round(dplot['AGE']).astype(int)
        
        fig = px.histogram(dplot, x='AGE', nbins=30, title=' 客戶年齡分布與性別占比',
                            color_discrete_map={  # 指定顏色映射
                            '男': 'rgb(0 ,104, 201)',
                            '女': 'rgb(131, 201 ,255)'
                        },color='SEXUAL',
                            labels={'SEXUAL': '性別','AGE':'年齡','count': '人數' }
                            )
        
        fig.update_layout(
            xaxis_title='年齡',
            yaxis_title='人數',
            bargap=0.1,  # 控制條形間距
            title_font_size=20,
            legend=dict(x=0.8, y=1.1, orientation='h', traceorder='reversed'),
            margin=dict(l=10, r=10, t=80, b=30),
        )
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        dplot = df.groupby('STUDENT_NO')['IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)'].max().reset_index()
        dplot = dplot['IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)'].value_counts().reset_index()
        dplot['IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)'].replace({'Old':'老客','New':'新客'},inplace=True)
        fig = px.pie(dplot,values='count' ,names='IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)',color='IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)',hole=.5,
                        color_discrete_map={  # 指定顏色映射
                            '新客': 'rgb(141, 211, 199)',
                            '老客': 'rgb(251, 128, 114)'
                        },
                       labels={'count': '人數','IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)':'客人狀態' })
        fig.update_traces(
                textinfo="percent+label",  # 顯示標籤和數值
                textposition='inside'  # 設置文字大小
            )
        fig.update_layout(
            title=' 新老客戶佔比',
            title_font_size=20,
            showlegend=False,
            margin=dict(l=10, r=10, t=80, b=30),
        )
        st.plotly_chart(fig,use_container_width=True)
    
    with col3:
        
        dplot = df.loc[df.groupby('STUDENT_NO_DETAIL_ITEM')['ORDER_TOTAL'].idxmax()]
        dplot = dplot.groupby(['IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)','INVOICE_NO'])['ORDER_TOTAL'].sum().reset_index()
        dplot = dplot.groupby('IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)')['ORDER_TOTAL'].mean().reset_index()
        dplot['IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)'].replace({'Old':'老客','New':'新客'},inplace=True)
        
        fig = px.bar(dplot,y='IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)',x='ORDER_TOTAL',orientation='h',
                        color='IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)',
                        color_discrete_map={  # 指定顏色映射
                            '新客': 'rgb(141, 211, 199)',
                            '老客': 'rgb(251, 128, 114)'
                        },
                        hover_data={'IS_OLD_CUSTOMER(IF PREVIOUS ORDER EXISTS)':False,'ORDER_TOTAL':':,.0f'},
                        labels={'ORDER_TOTAL': '客單價' }
                        )
        fig.update_layout(
            title=" 新老客戶客單價分析",
            title_font_size=20,
            showlegend=False,
            yaxis_title='',
            xaxis_title='客單價',
            margin=dict(l=10, r=10, t=80, b=30),
        )
        st.plotly_chart(fig,use_container_width=True)
with tab4:
    col1,col2 = st.columns([1,1.5])
    with col1:
        df_main = df[df['STATUS']=='本班']
        dplot = df_main.loc[df_main.groupby('STUDENT_NO_DETAIL_ITEM')['INVOICE_NO'].idxmax()]
        dplot = dplot.groupby('CLERK_NO')[['區域','ORDER_TOTAL','DISCOUNT_AMOUNT']].aggregate({'區域':'max','ORDER_TOTAL':['count','sum'],'DISCOUNT_AMOUNT':'sum'}).reset_index()
        dplot.columns = ['員工編號','區域','銷售數','銷售額','單客補貼']
        dplot['單客補貼'] = round(dplot['單客補貼']/dplot['銷售數'])
        dplot = dplot.sort_values('銷售額')
        st.dataframe(dplot.set_index('員工編號').sort_values('銷售額',ascending=False),use_container_width=True,height=420)
        
        if set(['北部', '中部', '南部', '其他']).issubset(dplot['區域'].unique()):
            category_order = ['北部','中部','南部','其他']
        else:
            category_order = list(dplot['區域'].unique())
        
    with col2:
        dplot['formatted_sales'] = dplot['銷售額'].apply(lambda x: f"{x:,}")
        fig = px.bar(dplot.tail(10),x='銷售額',y='員工編號',color='區域',orientation='h',text='formatted_sales',
                        color_discrete_sequence=px.colors.qualitative.Set3
                        ,category_orders={'區域': category_order},labels={'formatted_sales':'銷售額'})
        fig.update_layout(
            title = ' 銷售額Top 10員工',
            title_font_size=20,
            xaxis_visible = False,
            margin=dict(l=10, r=10, t=45, b=10
                        ),
        )
        fig.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=dplot['員工編號']  # 按排序後的員工編號順序
        )
        )
        st.plotly_chart(fig,use_container_width=True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig = px.histogram(dplot,x='銷售數',labels={'count': '人數'})
        fig.update_layout(
            title = ' 員工銷售數分布狀況',
            title_font_size=20,
            margin=dict(l=10, r=10, t=80, b=30),
            yaxis_title='人數',
        )
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        
        dplot = dplot.groupby('區域',group_keys=False).apply(lambda x:x.nlargest(3,'銷售數'))
        fig = px.bar(dplot,x='銷售數',y='員工編號',orientation='h',barmode='group',color='區域'
                        ,color_discrete_sequence=px.colors.qualitative.Set3
                        ,category_orders={'區域': category_order})
        fig.update_layout(
            title = '各區銷售TOP 3',
            title_font_size=20,
            margin=dict(l=10, r=10, t=80, b=30),
        )
        st.plotly_chart(fig,use_container_width=True)
        
        
with tab5:
    col1,col2 = st.columns(2)
    with col1:
        @st.fragment
        def my_fragment01():
            input_option = st.text_input("請新增區域名稱並用逗點分隔 ",placeholder="EX:北區,中區,南區")
            
            new_data = df_select.loc[df_select.groupby('LOCATION')['區域'].idxmax()][['LOCATION','區域']].reset_index(drop=True)
                
            options = list(set(input_option.split(",") + new_data['區域'].dropna().tolist()))
            data_update = st.data_editor(
                new_data,
                use_container_width=True,
                column_config={
                                '區域': st.column_config.SelectboxColumn(
                                    "區域",
                                    width = 'medium',
                                    options=options
                                    ),
                                })        
        # 定義按鈕觸發操作
            
            if st.button("儲存檔案"):
                data_update.to_csv(file_path, index=False)
                st.success(f"檔案已保存")
        my_fragment01()     
    
    @st.fragment
    def my_fragment01():
        df = px.data.iris()  # iris is a pandas DataFrame
        fig = px.scatter(df, x="sepal_width", y="sepal_length")

        event = st.plotly_chart(fig, key="iris", on_select="rerun")

        st.write(event)
    