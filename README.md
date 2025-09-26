# FashionApp

FashionApp basit bir Flask tabanlı REST API'sidir. Küçük bir moda kataloğunu sergiler, ürünleri listelemenize ve hafızada tutulan bir alışveriş sepetini yönetmenize olanak tanır.

## Kurulum

1. Bağımlılıkları yükleyin:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Geliştirme sunucusunu başlatın:

   ```bash
   flask --app app run --debug
   ```

   Sunucu varsayılan olarak `http://127.0.0.1:5000` üzerinde çalışacaktır.

## Uç noktalar

- `GET /health` – Servisin çalışır durumda olduğunu doğrulayan basit bir sağlık kontrolü.
- `GET /products` – Tüm ürün kataloğunu döndürür.
- `GET /products/<id>` – Tekil ürünü döndürür, bulunamazsa 404 döner.
- `POST /cart` – `product_id` ve opsiyonel `quantity` alanlarını içeren JSON gövdesiyle ürünü sepete ekler. Aynı ürün tekrar eklendiğinde miktarı artırılır.
- `GET /cart` – Sepetteki mevcut öğeleri ve ara toplamı listeler.
- `DELETE /cart` – Sepeti temizler.

## Testleri çalıştırma

Projeyle birlikte gelen pytest tabanlı bir test paketi vardır:

```bash
pytest
```

Tüm testlerin geçmesi uygulamanın temel akışlarının beklendiği gibi çalıştığını gösterir.
