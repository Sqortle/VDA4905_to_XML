# SOLID Prensipleri İçin Açıklama:

### Single Responsibility:
Bu prensip bir sınıfın değişmesi için tek bir sebep olmalıdır der.
Bunu sağlamak için önceden sadece VDA4905Converter ve SegmentsClass sınıflarından oluşan projeyi her sınıfın tek iş 
yapabilcek konuma getircek şekilde düzenledim.

##### Örnek:
Proje artık
VDADataParser,
XMLFormatter gibi tek iş yapan classlardan oluşuyor

### Open/Closed:
Yazılım varlıkları geliştirmeye açık, ancak değiştirmeye kapalı olmalıdır.
Önceden VDA segmentleri if kontrolleri ile kontrol ediliyordu. Bunun yerine
Her segment için yeni bir class açıldı ve bu şekilde yeni bir segment eklenmesi
gerekirse class içinde değişiklik yapmak yerine yeni class 
açılıyor.

##### Örnek:
515 segmentini eklemek için Segment513Processor,
Segment513Processor classlarında değişiklik yapılmayacak 
yeni bir Segment515Processor classı eklenecek

### Liskov Substition:
Türetilmiş sınıflar, temel sınıfların yerine geçebilmelidir
Segment51XProcessor sınıfları ISegmentProcessor arayüzünü uyguluyor
ve bunun sayesinde VDA4905Converter sınıfı işlemcileri arayüz tipi
olarak ele alır ve hangi somut işlemci sınıfı olursa olsun
process() metodunu güvenle çağırabilir.
Bir de 514 sınıfı 513 le neredeyse aynı işi yaptığı için 513'ü 
miras alıyor.

### Interface Segregation:
IsegmentProcessor arayüzü yalnızca segment işlemeye odaklanan tek bir metod 
tanımlıyor. Bu Processor sınıflarının, kendiyle ilgili olmayan
metotları uygulamaya zorlamasını engeller.

### Dependency Inversion:
Yüksek seviyeli modüller, düşük seviyeli modüllere değil,
soyutlamalara bağımlı olmalıdır.
VDA4905Converter(yüksek seviye) doğrudan somut işlemci sınıflarına
bağımlı olmak yerine ISegmentProccessor arayüzüne bağımlıdır.
Processorler PROCESSORS sözlüğü aracılığıyla arayüz olarak kullanılır.

