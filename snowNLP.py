from snownlp import SnowNLP, sentiment
import csv


# 使用snownlp情感分析
def read_and_analysis(input_file, output_file):
    f = open(input_file, 'r')
    fw = open(output_file, "w", newline='')
    corpus = csv.reader(f)
    for row in corpus:
        ss = str(row[1]).replace(',', '，')
        s = SnowNLP(ss)
        fw.write(row[0] + ',')
        fw.write(ss + ',')
        for i in s.words:
            fw.write(i + ';')
        fw.write(',')
        fw.write(str(s.sentiments) + ',')
        if s.sentiments >= 0.2:
            fw.write('positive')
        else:
            fw.write('negative')
        fw.write('\n')
    fw.close()
    f.close()


# 生成negative和positive的数据集
def get_neg_pos_txt():
    f = open(r'Data/TrainingData/TrainingDataSet.csv', 'r', encoding='utf-8')
    f_neg =open(r'Data/Output/neg.txt','w',newline='', encoding='utf-8')
    f_pos =open(r'Data/Output/pos.txt','w',newline='', encoding='utf-8')
    corpus = csv.reader(f)
    lines = 0
    for row in corpus:
        if lines == 0:
            lines += 1
            continue
        sentence = row[1]
        score = str(row[4]).strip().split(';')[:-1]
        if(score==[]):
            continue
        else:
            sum=0
            for i in score:
                sum+=int(i)
            if(sum>=0):
                f_pos.write(sentence)
                f_pos.write('\n')
            else:
                f_neg.write(sentence)
                f_neg.write('\n')
    f.close()
    f_neg.close()
    f_pos.close()


# 利用新的数据训练情感分析模型
def train_my_data():
    # 重新训练模型
    sentiment.train(r'Data/Output/neg.txt', r'Data/Output/pos.txt')
    # 保存好新训练的模型
    sentiment.save(r'Data/Output/sentiment.marshal')


if __name__ == "__main__":
    input_file = r'Data/TestingData/TestingDataSet.csv'
    output_file = r'Data/Output/result_2.csv'
    # get_neg_pos_txt()
    # train_my_data()
    read_and_analysis(input_file, output_file)
