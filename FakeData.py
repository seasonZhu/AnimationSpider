import faker

def fakeData():
    fake = faker.Faker(locale='zh_CN')

    jasperId = ["101842918", "101200123", "101842000", "1112311342", "123422323"]

    date = "20210318"

    for i in range(len(jasperId)):
        for j in range(100):
            iccid = fake.random_number(digits = 20)
            sim = fake.random_number(digits = 11)
            msisdn = "86" + str(sim)
            imsi = "4600" + str(sim)
            string = jasperId[i] + "\t" + date + "\t" + str(iccid) + "\t"+ imsi + "\t" + msisdn + "\t" + "10\n"

            with open ("esim.txt", "a+") as fp:
                fp.write(string)

if __name__ == "__main__":
    fakeData()