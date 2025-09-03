import pandas as pd
from datetime import datetime, timedelta

def read_data(file_path):
    return pd.read_csv(file_path)

def check_data(data):
    if data is None:
        return False
    if data.empty:
        return False
    return True

def check_date_continuity(file_path, date_column='date'):
    """
    检查CSV文件中的日期是否有断层
    
    Args:
        file_path (str): CSV文件路径
        date_column (str): 日期列名，默认为'date'
    
    Returns:
        dict: 包含检查结果的字典
    """
    try:
        # 读取数据
        df = pd.read_csv(file_path)
        
        if df.empty:
            return {
                'status': 'error',
                'message': '数据文件为空'
            }
        
        # 确保日期列存在
        if date_column not in df.columns:
            return {
                'status': 'error',
                'message': f'找不到日期列: {date_column}'
            }
        
        # 转换日期格式
        df[date_column] = pd.to_datetime(df[date_column])
        
        # 按日期排序
        df = df.sort_values(date_column)
        
        # 获取所有日期
        dates = df[date_column].dt.date.tolist()
        
        # 检查日期断层
        missing_dates = []
        gaps = []
        
        for i in range(1, len(dates)):
            current_date = dates[i]
            previous_date = dates[i-1]
            
            # 计算日期差
            date_diff = (current_date - previous_date).days
            
            # 如果日期差大于1天，说明有断层
            if date_diff > 1:
                # 找出缺失的日期
                missing_start = previous_date + timedelta(days=1)
                missing_end = current_date - timedelta(days=1)
                
                gap_info = {
                    'gap_start': previous_date,
                    'gap_end': current_date,
                    'missing_days': date_diff - 1,
                    'missing_dates': []
                }
                
                # 生成缺失的日期列表
                temp_date = missing_start
                while temp_date <= missing_end:
                    gap_info['missing_dates'].append(temp_date)
                    temp_date += timedelta(days=1)
                
                gaps.append(gap_info)
                missing_dates.extend(gap_info['missing_dates'])
        
        # 返回检查结果
        result = {
            'status': 'success',
            'total_records': len(df),
            'date_range': {
                'start': dates[0],
                'end': dates[-1]
            },
            'has_gaps': len(gaps) > 0,
            'total_gaps': len(gaps),
            'total_missing_days': len(missing_dates),
            'gaps': gaps,
            'missing_dates': missing_dates
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'检查过程中出现错误: {str(e)}'
        }

def print_date_check_result(result):
    """
    打印日期检查结果的详细信息
    """
    if result['status'] == 'error':
        print(f"❌ 检查失败: {result['message']}")
        return
    
    print(f"📊 数据概览:")
    print(f"   总记录数: {result['total_records']}")
    print(f"   日期范围: {result['date_range']['start']} 至 {result['date_range']['end']}")
    
    if result['has_gaps']:
        print(f"\n⚠️  发现日期断层:")
        print(f"   断层数量: {result['total_gaps']}")
        print(f"   缺失天数: {result['total_missing_days']}")
        
        print(f"\n📅 断层详情:")
        for i, gap in enumerate(result['gaps'], 1):
            print(f"   断层 {i}: {gap['gap_start']} 到 {gap['gap_end']} (缺失 {gap['missing_days']} 天)")
            if len(gap['missing_dates']) <= 10:  # 如果缺失日期不多，显示具体日期
                print(f"      缺失日期: {', '.join([str(d) for d in gap['missing_dates']])}")
            else:  # 如果缺失日期很多，只显示前几个
                print(f"      缺失日期: {', '.join([str(d) for d in gap['missing_dates'][:5]])} ... (共{len(gap['missing_dates'])}天)")
    else:
        print(f"\n✅ 日期连续，无断层")

