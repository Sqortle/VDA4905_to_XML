# SOLID Prensipleri İçin Açıklama: 

## Single Responsibility: 

Bu prensip bir sınıfın değişmesi için tek bir sebep olmalıdır der. Bunu sağlamak için önceden sadece VDA4905Converter ve SegmentsClass sınıflarından oluşan projeyi her sınıfın tek iş yapabilcek konuma getircek şekilde düzenledim.

### Örnek: 

Proje artık VDADataParser, XMLFormatter gibi tek iş yapan classlardan oluşuyor

## Open/Closed:

Yazılım varlıkları geliştirmeye açık, ancak değiştirmeye kapalı olmalıdır. Önceden VDA segmentleri if kontrolleri ile kontrol ediliyordu. Bunun yerine Her segment için yeni bir class açıldı ve bu şekilde yeni bir segment eklenmesi gerekirse class içinde değişiklik yapmak yerine yeni class açılıyor.

### Örnek: 

515 segmentini eklemek için Segment513Processor, Segment513Processor classlarında değişiklik yapılmayacak yeni bir Segment515Processor classı eklenecek

## Liskov Substition: 

Türetilmiş sınıflar, temel sınıfların yerine geçebilmelidir Segment51XProcessor sınıfları ISegmentProcessor arayüzünü uyguluyor ve bunun sayesinde VDA4905Converter sınıfı işlemcileri arayüz tipi olarak ele alır ve hangi somut işlemci sınıfı olursa olsun process() metodunu güvenle çağırabilir. Bir de 514 sınıfı 513 le neredeyse aynı işi yaptığı için 513'ü miras alıyor.

## Interface Segregation: 

IsegmentProcessor arayüzü yalnızca segment işlemeye odaklanan tek bir metod tanımlıyor. Bu Processor sınıflarının, kendiyle ilgili olmayan metotları uygulamaya zorlamasını engeller.

## Dependency Inversion: 

Yüksek seviyeli modüller, düşük seviyeli modüllere değil, soyutlamalara bağımlı olmalıdır. VDA4905Converter(yüksek seviye) doğrudan somut işlemci sınıflarına bağımlı olmak yerine ISegmentProccessor arayüzüne bağımlıdır. Processorler PROCESSORS sözlüğü aracılığıyla arayüz olarak kullanılır.

# Factory Design:

Proje Factory Design Pattern'e göre düzenlendi. Bu deseni kullanmamın
sebebi projenin modülerliğini ve sürdürülebirliğini sağlamaktı.

## Temel Rolü:

Her gelen VDA segmentinin kendine ait özel bir işlemcisi var.
Factory Design, bu segment tiplerine karşılık gelen işlemci nesnelerinin
yaratılma mantığını ana dönüştürücü bölümünden ayırıyor.

## Neler Yapıldı:

1. Nesne yaratma işi SegmentProcessorFactory sınıfına devredildi.
2. VDA4905Conerter sınıfı hangi segment için hangi sınıfı oluşturucağını bilmek zorunda değil. Sadece Factory'ye soruyor.

# Singleton Design:

Projede mimariyi optimize etmek ve kaynak kullanımını kontrol altına almak amacıyla
Singleton Desgn Pattern kullanıldı.

## Temel Rolü:

Singleton design, bir sınıfın uygulama boyunca yalnızca tek bir örneğinin (instance) var olmasını garanti eder. Bu, özellikle her program çevrimi veya her çağrıda defalarca örneklense bile, her zaman aynı nesneyi kullanmak istediğimiz sınıflar için idealdir.

## Hangi Sınıflarda Kullanıldı:

1. XMLFormatter: XML yapısını okunur hale getirmek için girintileme (indent) işini yapan sınıftır. Durum tutmadığı için, tek bir örneğin olması gereksiz bellek kullanımını önler.
2. FileHandler: Oluşturulan XML dosyasını diske yazma işini yapan sınıftır. Bu kaynağa tek bir noktadan erişimi kontrol etmek, hem temizlik hem de verimlilik sağlar.

## Naıl Yapıldı:

Bu sınıfların yapıcı metodunu (\_\_new__) özel hale getirilerek, sınıfın kendisinin daha önce bir örnek oluşturulup oluşturulmadığını kontrol etmesi sağlandı. Eğer yoksa oluşturur, varsa mevcut örneği geri döndürür.

