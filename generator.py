import sys
import yaml

class Statement:

    def __init__(self, table, fields):
        self.table = table.lower()
        self.fields = fields
        self.result = []

    def create_statement(self):
        self.result.append("CREATE TABLE \"%s\" (\n\t\"%s_id\" SERIAL PRIMARY KEY NOT NULL,"%(table,column))
        self.result.append("\n\t\"{}_created\" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,".format(self.table))
        self.result.append("\n\t\"{}_updated\" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,".format(self.table))

    def add_fields(self):
        field_values = self.fields.get('fields')

        for key, value in field_values.iteritems():        
            self.result.append("\n\t\"{}_{}\" {} NOT NULL,".format(self.table, key, value))

        self.result[-1] = (self.result[-1])[:-1] + ' );'

    def add_trigger(self):
        self.result.append("\nCREATE OR REPLACE FUNCTION update() RETURNS TRIGGER AS")
        self.result.append("\n\t'BEGIN NEW.updated = NOW();\n\tRETURN NEW; \n\tEND;\n\t'LANGUAGE 'plpgsql';")
        self.result.append("\nCREATE TRIGGER update_trigger BEFORE UPDATE ON \"{}\" "
                           "FOR EACH ROW EXECUTE PROCEDURE update();\n\n".format(self.table))


    def get_result(self):
        self.create_statement()
        self.add_fields()
        self.add_trigger()

        return "".join(self.result)

    def get_table(self):
        return self.table

    def get_fields(self):
        return self.fields


def main():
    file_name = raw_input("Enter file name: ")
    file_in = open(file_name, 'r')
    file_out = open("result.sql", 'w')
    text = yaml.load(file_in)

    for key, value in text.iteritems():
        statement = Statement(key, value)
        file_out.write(statement.get_result())

    file_in.close()
    file_out.close()    

if __name__ == "__main__":
    main()