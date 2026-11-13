from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///shedules.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Equipment(Base):
    "Создание таблицы"
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, name="№ п/п")
    name_equipment = Column(String(100), nullable=True, name="Наименование ТУ (марка, тип)")
    factory_number = Column(String(100), nullable=True, name="Заводской номер")
    manufacture_date = Column(String(15), nullable=True, name="Год изготовления")
    work_type = Column(String(50), nullable=True, name="Вид работ")
    location = Column(String(200), nullable=True, name="Местонахождение")
    epb_date = Column(String(20), name="Дата ЭПБ")
    note = Column(String(255), nullable=True, name="Примечания")

    def __repr__(self):
        return (f"| Наименование ТУ (марка, тип): {self.name_equipment} | "
                f"Заводской номер: {self.factory_number} | "
                f"Год изготовления: {self.manufacture_date} | "
                f"Вид работ: {self.work_type} | " 
                f"Местонахождение: {self.location} | "
                f"Дата ЭПБ: {self.epb_date} |"
                f"Примечания: {self.note}")

def drop_tables(team_names):
    """Удаляет указанные таблицы из БД, если они существуют"""
    # Сначала регистрируем кламмы с правильными __tablename__, чтобы Base.metadata "увидел" эти таблицы
    tables_to_drop = []
    for name in team_names:
        class_name = f"Equipment_{name}"
        DynamicClass = type(
            class_name,
            (Equipment,),
            {
                "__tablename__": name,
                "__module__": __name__,
                "__table_args__": {"extend_existing": True}
            },
        )
        table = Base.metadata.tables.get(name)
        if table is not None:
            tables_to_drop.append(table)
    
    if tables_to_drop:
        Base.metadata.drop_all(engine, tables=tables_to_drop)
        print(f"✅ Удалены таблицы: {[t.name for t in tables_to_drop]}")
    else:
        print("ℹ️ Нет таблиц для удаления.")


def create_table_for_team(team_name):
    """Создает таблицу для конкретной компании"""
    # Динамически создаём класс для таблицы
    class_name = f"Equipment_{team_name}"
    dynamic_class = type(
        class_name,
        (Equipment,),
        {
            "__tablename__": team_name,
            "__module__": __name__,
            "__table_args__": {"extend_existing": True}
        }
    )
    
    # Создаёт таблицу
    Base.metadata.create_all(engine)
    
    return dynamic_class


def adding_data(name, number, manufacture_date, work_type, location, epb_date, note, team_name):
    "Добавляет значения в таблицу"
    
    dynamic_class = create_table_for_team(team_name)
    
    new_data = dynamic_class(
        name_equipment=name,
        factory_number=number,
        manufacture_date=manufacture_date,
        work_type=work_type,
        location=location,
        epb_date=epb_date,
        note=note,
    )
    session.add(new_data)
    session.commit()
