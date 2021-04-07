import pandas as pd
import numpy as np
import pandasgui
import matplotlib.pyplot as plt
import sqlite3


def main():

    #zadanie 1:

    years_range = range(1880, 2019+1)
    temp = []
    allData = []

    #load data
    for year in years_range:
        path = 'names\yob{}.txt'.format(year)
        columns = ['name', 'gender', 'birthcount']
        df = pd.read_csv(path, names=columns)
        df['year']=year
        temp.append(df)
        allData = pd.concat(temp, ignore_index=True)

    ####################################################

    #zadanie 2:

    print("---------- ZADANIE 2 ----------\n")

    unique_names = allData.pivot_table(allData,index=['name'],aggfunc=lambda x: len(x.unique()))
    print(f'W danym zakresie czasu nadano {len(unique_names)} unikalnych imion.\n')

    ####################################################

    #zadanie 3:

    print("---------- ZADANIE 3 ----------\n")


    girls = allData.loc[allData["gender"] == 'F', :]
    girls_unique_names = girls.pivot_table(girls,index=['name'],aggfunc=lambda x: len(x.unique()))

    boys = allData.loc[allData["gender"] == 'M', :]
    boys_unique_names = boys.pivot_table(boys,index=['name'],aggfunc=lambda x: len(x.unique()))

    print(f'W danym zakresie czasu nadano:\n{len(girls_unique_names)} unikalnych imion żeńskich,\n'
          f'{len(boys_unique_names)} unikalnych imion męskich.\n')

    ####################################################

    #zadanie_4:
    girl_total_births = []
    male_total_births = []
    girl_total_births = girls.pivot_table(girls, index=['year'], aggfunc=sum)
    male_total_births = boys.pivot_table(boys, index=['year'], aggfunc=sum)
    total_births = girl_total_births + male_total_births

    allData['frequency_female'] = 0
    allData['frequency_male'] = 0

    for y in years_range:

        var_g = girls.loc[girls["year"] == y]
        freq_g = (var_g['birthcount'] / girl_total_births['birthcount'][y])*100
        allData['frequency_female'].update(freq_g)

        var_m = boys.loc[boys["year"] == y]
        freq_m = (var_m['birthcount'] / male_total_births['birthcount'][y])*100
        allData['frequency_male'].update(freq_m)

    ####################################################

    #Zadanie_5:

    print("---------- ZADANIE 5 ----------\n")

    total_births = allData.pivot_table(allData, index=['year'], aggfunc=sum)

    ratio = girl_total_births/male_total_births

    fig, ax = plt.subplots(2)
    ax[0].set_title('Liczba urodzin w danym roku.')
    ax[0].plot(years_range,total_births["birthcount"],color = 'red')
    ax[1].set_title('Stosunek liczby narodzin dziewczynek do liczby narodzin chłopców.')
    ax[1].plot(years_range, ratio["birthcount"])


    ax[1].set_xlabel('Rok')
    ax[0].set_ylabel('Liczba urodzin')
    ax[1].set_ylabel('Stosunek narodzin F/M')


    print('Największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami zanotowano w 1901 roku,'
          ' natomiast najmmniejszą w 1880.\n')

    ####################################################

    #Zadanie_6:

    print("---------- ZADANIE 6 ----------\n")

    vec_f = []
    vec_m = []

    for y in years_range:
        sort_m = boys.loc[boys["year"] == y].sort_values('birthcount',ascending=False)
        top1000_m = sort_m.iloc[0:1000, :]
        vec_m.append(top1000_m)

        sort_f = girls.loc[girls["year"] == y].sort_values('birthcount',ascending=False)
        top1000_f = sort_f.iloc[0:1000, :]
        vec_f.append(top1000_f)

    most_popular_female_names_all_years = pd.concat(vec_f, ignore_index=True)
    data_f = most_popular_female_names_all_years.pivot_table('birthcount',index=['name'],aggfunc=sum)
    data_f.sort_values('birthcount',inplace=True,ascending=False)
    #TOP 1000 F:
    sorted_f = data_f.iloc[0:1000,:]
    print('TOP 1000 imion żeńskich:\n',sorted_f,'\n')


    most_popular_male_names_all_years = pd.concat(vec_m, ignore_index=True)
    data_m = most_popular_male_names_all_years.pivot_table('birthcount',index=["name"],aggfunc=sum)
    data_m.sort_values('birthcount',inplace=True,ascending=False)
    #TOP 1000 M:
    sorted_m = data_m.iloc[0:1000,:]
    print('TOP 1000 imion męskich:\n',sorted_m,'\n')


    #TOP for M i F
    vector_top2000 = []
    vector_top2000.append(sorted_f)
    vector_top2000.append(sorted_m)
    df_top2000 = pd.concat(vector_top2000)
    df_top2000 = df_top2000.pivot_table('birthcount',index=["name"],aggfunc=sum)
    df_top2000.sort_values('birthcount', inplace=True, ascending=False)

    ####################################################

    #Zadanie 7

    print("---------- ZADANIE 7 ----------\n")

    names = ['James', 'Mary', 'Harry', 'Marilin']

    data_James = allData.loc[(allData["name"] == names[0]) & (allData["gender"] == 'M')]
    birthcount_James = data_James.loc[:, "birthcount"]
    frequency_James = data_James.loc[:, "frequency_male"]
    year_James = data_James.loc[:, "year"]

    data_Mary = allData.loc[(allData["name"] == names[1]) & (allData["gender"] == 'F')]
    birthcount_Mary = data_Mary.loc[:, "birthcount"]
    frequency_Mary = data_Mary.loc[:, "frequency_female"]
    year_Mary = data_Mary.loc[:, "year"]

    data_Harry = allData.loc[(allData["name"] == names[2]) & (allData["gender"] == 'M')]
    birthcount_Harry = data_Harry.loc[:, "birthcount"]
    frequency_Harry = data_Harry.loc[:, "frequency_male"]
    year_Harry = data_Harry.loc[:, "year"]

    data_Marilin = allData.loc[(allData["name"] == names[3]) & (allData["gender"] == 'F')]
    birthcount_Marilin = data_Marilin.loc[:, "birthcount"]
    frequency_Marilin = data_Marilin.loc[:, "frequency_female"]
    year_Marilin = data_Marilin.loc[:, "year"]

    fig, ax1 = plt.subplots()
    ax1.set_title('Wykresy zmian dla imion: James, Mary, Harry, Marilin')

    ax1.plot(year_James,birthcount_James)
    ax1.plot(year_Mary,birthcount_Mary)
    ax1.plot(year_Harry,birthcount_Harry)
    ax1.plot(year_Marilin,birthcount_Marilin)

    ax2 = ax1.twinx()
    ax2.plot(year_James,frequency_James,'.')
    ax2.plot(year_Mary,frequency_Mary,'.')
    ax2.plot(year_Harry,frequency_Harry,'.')
    ax2.plot(year_Marilin,frequency_Marilin,'.')

    ax1.legend(['James', 'Mary', 'Harry','Marilin'],loc='center left')
    ax2.legend(['James', 'Mary', 'Harry','Marilin'],loc='center right')
    ax1.set_xlabel('Rok')
    ax1.set_ylabel('Liczba nadanych imion')
    ax2.set_ylabel('Popularność')


    check1 = data_James.loc[(data_James["year"]==1940)]
    check2 = data_James.loc[(data_James["year"]==1980)]
    check3 = data_James.loc[(data_James["year"]==2019)]
    print("Imię James nadano:")
    print(f'{check1["birthcount"].values[0]} razy w roku 1940,')
    print(f'{check2["birthcount"].values[0]} razy w roku 1980,')
    print(f'{check3["birthcount"].values[0]} razy w roku 2019.\n')

    check1 = data_Mary.loc[(data_Mary["year"]==1940)]
    check2 = data_Mary.loc[(data_Mary["year"]==1980)]
    check3 = data_Mary.loc[(data_Mary["year"]==2019)]
    print("Imię Mary nadano:")
    print(f'{check1["birthcount"].values[0]} razy w roku 1940,')
    print(f'{check2["birthcount"].values[0]} razy w roku 1980,')
    print(f'{check3["birthcount"].values[0]} razy w roku 2019.\n')

    check1 = data_Harry.loc[(data_Harry["year"]==1940)]
    check2 = data_Harry.loc[(data_Harry["year"]==1980)]
    check3 = data_Harry.loc[(data_Harry["year"]==2019)]
    print("Imię Harry nadano:")
    print(f'{check1["birthcount"].values[0]} razy w roku 1940,')
    print(f'{check2["birthcount"].values[0]} razy w roku 1980,')
    print(f'{check3["birthcount"].values[0]} razy w roku 2019.\n')

    check2 = data_Marilin.loc[(data_Marilin["year"]==1980)]
    check3 = data_Marilin.loc[(data_Marilin["year"]==2019)]
    print("Imię Marilin nadano:")
    print('0 razy w roku 1940,')
    print(f'{check2["birthcount"].values[0]} razy w roku 1980,')
    print(f'{check3["birthcount"].values[0]} razy w roku 2019.\n')

    ####################################################

    #Zadanie 8:

    print("---------- ZADANIE 8 ----------\n")

    pd.options.mode.chained_assignment = None

    boys["isTop1000"] = None
    select_top1000_m = boys.loc[:,["name"]].isin(sorted_m.index)
    boys.loc[:,["isTop1000"]] = select_top1000_m.values
    select_true_m = boys.loc[boys["isTop1000"]== True,:]
    data_m = select_true_m.pivot_table('birthcount',index=['year'],aggfunc=sum)


    girls["isTop1000"] = None
    select_top1000_f = girls.loc[:,["name"]].isin(sorted_f.index)
    girls.loc[:,["isTop1000"]] = select_top1000_f.values
    select_true_f = girls.loc[girls["isTop1000"]== True,:]
    data_f = select_true_f.pivot_table('birthcount',index=['year'],aggfunc=sum)

    percent_m = ((data_m/male_total_births) * 100)
    percent_f = ((data_f/girl_total_births) * 100)


    fig, ax3 = plt.subplots()
    ax3.plot(percent_m.index,percent_m.values)
    ax3.plot(percent_f.index, percent_f.values)

    ax3.set_title("Różnorodność imion")
    ax3.legend(['M', 'F'])
    ax3.set_xlabel('Rok')
    ax3.set_ylabel('Imiona należące do rankingu top1000 [%]')

    zmienna = abs(percent_m-percent_f)
    # print(zmienna)
    print("Największą różnicę w różnorodności między imionami męskimi a żeńskimi zaobserwowano w 2011 roku.\n")

    ####################################################

    #Zadanie 9

    print("---------- ZADANIE 9 ----------\n")

    #select male data
    boys = allData.loc[allData["gender"] == 'M', :]
    male_total_births = boys.pivot_table("birthcount", index=['year'], aggfunc=sum)

    #total number of births in years: 1910,1960,2015
    total_births1910 = male_total_births.loc[male_total_births.index==1910,:]
    total_births1960 = male_total_births.loc[male_total_births.index==1960,:]
    total_births2015 = male_total_births.loc[male_total_births.index==2015,:]

    #select the last letter of the name and entering the value into a new column
    temp = allData["name"].str.get(-1)
    allData["Last_letter"] = None
    allData.loc[:,["Last_letter"]] = temp.values

    #occurrence of the each letter each year
    select_1910 = allData.loc[(allData["year"] == 1910) & (allData["gender"] == 'M'),:]
    letter_1910 = select_1910.pivot_table("birthcount", index = ["Last_letter"], aggfunc= sum)

    select_1960 = allData.loc[(allData["year"] == 1960) & (allData["gender"] == 'M'),:]
    letter_1960 = select_1960.pivot_table("birthcount", index = ["Last_letter"], aggfunc= sum)

    select_2015 = allData.loc[(allData["year"] == 2015) & (allData["gender"] == 'M'),:]
    letter_2015 = select_2015.pivot_table("birthcount", index = ["Last_letter"], aggfunc= sum)

    data = letter_2015
    data["birth1960"] = letter_1960["birthcount"]
    data["birth1910"] = letter_1910["birthcount"]

    #setting the value of missing letters in 1910 and 1960 to 0
    data.loc[data.index == 'j',"birth1910"] = 0
    data.loc[data.index == 'q',"birth1910"] = 0
    data.loc[data.index == 'j', "birth1960"] = 0
    data.loc[data.index == 'q', "birth1960"] = 0

    #normalization of data in relation to the total number of births in a given year
    result_1910 = data["birth1910"].values/total_births1910.values
    result_1960 = data["birth1960"].values/total_births1960.values
    result_2015 = data["birthcount"].values/total_births2015.values

    #difference between 1910 and 2015
    result = abs(result_1910 - result_2015) / result_2015

    data['difference'] = ""
    data["difference"] = result[0]

    #plot data
    fig, ax4 = plt.subplots()
    x = np.arange(len(letter_2015.index))
    width = 0.3
    labels = [str(i) for i in letter_2015.index]

    ax4.bar(x-width, result_1910[0], width, label='1910')
    ax4.bar(x, result_1960[0], width, label='1960')
    ax4.bar(x+width, result_2015[0], width, label='2015')

    ax4.set_xticks(x)
    ax4.set_xticklabels(labels)

    ax4.set_title("Popularność liter (dla mężczyzn)")
    ax4.legend(['1910', '1960','2015'])
    ax4.set_xlabel('Litera')
    ax4.set_ylabel('Popularność')


    print("Największą różnicę miedzy rokiem 1910 a 2015 zaobserwowano dla litery d.\n")


    # select data d,p,t

    d = allData.loc[(allData["Last_letter"] == 'd') & (allData["gender"] == 'M'),:]
    letter_d = d.pivot_table("birthcount", index = ["year"], aggfunc= sum)
    result_d = letter_d/male_total_births

    p = allData.loc[(allData["Last_letter"] == 'p') & (allData["gender"] == 'M'),:]
    letter_p = p.pivot_table("birthcount", index = ["year"], aggfunc= sum)
    result_p = letter_p/male_total_births

    t = allData.loc[(allData["Last_letter"] == 't') & (allData["gender"] == 'M'),:]
    letter_t = t.pivot_table("birthcount", index = ["year"], aggfunc= sum)
    result_t = letter_t/male_total_births

    # plt.figure()
    fig, ax5 = plt.subplots()
    ax5.plot(result_d.index,result_d.values)
    ax5.plot(result_p.index, result_p.values)
    ax5.plot(result_t.index, result_t.values)
    ax5.set_title("Przebieg trendu popularności dla liter d,p,t")
    ax5.legend(['d', 'p', 't'])
    ax5.set_xlabel('Rok')
    ax5.set_ylabel('Popularność')

    ####################################################

    #Zadanie 10

    print("---------- ZADANIE 10 ----------\n")

    boys = allData.loc[allData["gender"] == 'M', :]
    girls["isMale"] = None
    select_f = girls.loc[:,["name"]].isin(boys["name"].values)
    girls.loc[:,["isMale"]] = select_f.values
    select_true_f = girls.loc[girls["isMale"]== True,:]
    select_true = select_true_f.pivot_table("birthcount", index=["name"], aggfunc=sum)
    select_true.sort_values('birthcount', inplace = True, ascending = False)

    print("Najpopularniejsze imię męskie i żeńskie to James.\n")

    ####################################################

    #Zadanie 11

    print("---------- ZADANIE 11 ----------\n")

    data = allData.loc[:,["name"]].isin(select_true.index)
    allData["unisex"] = None
    allData.loc[:, ["unisex"]] = data.values
    select_true_all = allData.loc[allData["unisex"] == True, :]
    selectTrue = select_true_all.pivot_table(select_true_all, index=["year", "name"],aggfunc=sum)
    selectTrue["popularity"] = 0

    res = ((selectTrue["frequency_male"].values)/(selectTrue["frequency_male"].values + selectTrue["frequency_female"].values))
    selectTrue["popularity"]=res

    years_earlier = selectTrue.loc[1880:1920, :]
    years_later = selectTrue.loc[2000:2020, :]
    years_earlier_pivot = years_earlier.pivot_table("popularity", index=["name"], aggfunc= np.average)
    years_later_pivot = years_later.pivot_table("popularity", index=["name"], aggfunc=np.average)

    early_pop_max = years_earlier_pivot.loc[years_earlier_pivot["popularity"]>0.7,:]
    late_pop_min = years_later_pivot.loc[years_later_pivot["popularity"]<0.3,:]

    early_pop_min = years_earlier_pivot.loc[years_earlier_pivot["popularity"]<0.3,:]
    late_pop_max = years_later_pivot.loc[years_later_pivot["popularity"]>0.7,:]


    vector_df = []

    select_early = (late_pop_min.index).isin(early_pop_max.index)
    late_pop_min["Check"] = None
    late_pop_min.loc[:,["Check"]] = select_early
    early_true = late_pop_min.loc[late_pop_min["Check"]== True,:]
    vector_df.append(early_true)

    select_later = (early_pop_min.index).isin(late_pop_max.index)
    early_pop_min["Check"] = None
    early_pop_min.loc[:,["Check"]] = select_later
    later_true = early_pop_min.loc[early_pop_min["Check"]== True,:]
    vector_df.append(later_true)

    df = pd.concat(vector_df)

    select_top2000 = (df_top2000.index).isin(df.index)
    df_top2000["isTOP"] = None
    df_top2000.loc[:,["isTOP"]] = select_top2000
    pop_name = df_top2000.loc[df_top2000["isTOP"]== True,:]
    pop_name = pop_name.reset_index(level=['name'])
    # print(pop_name.loc[0]["name"])
    # print(pop_name.loc[1]["name"])

    print(f'Dwa najpopularniejsze imiona, które przez pewien czas były imionami żeńskimi/męskimi,'
          f' a następnie stały się imionami męskimi/żeńskimi to {pop_name.loc[0]["name"]} oraz {pop_name.loc[1]["name"]}.\n')

    data = selectTrue.reset_index(level=['name'])

    Ashley = data.loc[data["name"]=="Ashley",:]
    Kelly = data.loc[data["name"]=="Kelly",:]

    fig, ax6 = plt.subplots()
    ax6.plot(Ashley.index,Ashley["popularity"].values)
    ax6.plot(Kelly.index,Kelly["popularity"].values)
    ax6.legend(['Ashley', 'Kelly'])
    ax6.set_title("Przebieg trendu dla imion Ashley oraz Kelly")
    ax6.set_xlabel('Rok')
    ax6.set_ylabel('Wsp. popularności')

    ####################################################

    #Zadanie 12

    conn = sqlite3.connect("USA_ltper_1x1.sqlite")  # połączenie do bazy danych - pliku
    tables_df = pd.read_sql('SELECT * FROM USA_fltper_1x1 UNION ALL SELECT * FROM USA_mltper_1x1', conn)
    conn.close()

    ####################################################

    #Zadanie 13

    total_births = allData.pivot_table("birthcount", index=['year'], aggfunc=sum)

    dx = tables_df.pivot_table("dx",index=["Year"],aggfunc=sum)

    births = total_births.loc[1959 :2017,:]
    birthrate = births['birthcount'] - dx['dx']

    # print("Przyrost naturalny:")
    # print(birthrate)

    fig, ax7 = plt.subplots()
    ax7.plot(births.index,birthrate)
    ax7.set_title("Przyrost naturalny w latach 1959-2018")
    ax7.set_xlabel('Rok')
    ax7.set_ylabel('Wsp. popularności')

    ####################################################

    #Zadanie 14
    years_range2 = range(1959,2018)

    vec_first_year = []

    dx_14 = tables_df.pivot_table("dx",index=["Year","Age"],aggfunc=sum)
    for year in years_range2:
        z = dx_14.loc[year, 0]["dx"]
        vec_first_year.append((((total_births.loc[year]["birthcount"]) - z) / total_births.loc[year]["birthcount"])*100)

    fig, ax8 = plt.subplots()
    ax8.plot(years_range2, vec_first_year)
    ax8.set_title("Współczynnik przeżywalności dzieci w pierwszym roku życia")
    ax8.set_xlabel('Rok')
    ax8.set_ylabel('Wsp. przeżywalności [%]')

    ####################################################

    #Zadanie 15

    vec_five_year = []

    dx_15 = tables_df.pivot_table("dx", index=["Year","Age"], aggfunc=sum)
    z= 0

    for year in years_range2[:-5]:
        for i in range(0,5):
            z+= dx_15.loc[year+i, i]["dx"]
        vec_five_year.append((((total_births.loc[year]["birthcount"])- z)/total_births.loc[year]["birthcount"])*100)
        z = 0

    fig, ax9 = plt.subplots()
    ax9.set_title("Współczynnik przeżywalności dzieci")
    ax9.plot(years_range2, vec_first_year)
    ax9.plot(years_range2[:-5],vec_five_year)
    ax9.legend(["1","5"])


    ####################################################
    # pandasgui.show(allData, settings={'block': True})

    plt.show()


if __name__ =="__main__":
    main()