# Online-Book-Library

წიგნების ელექტრონული სარჩევი, რაც გულისხმობს სხვადასხვა საიტებიდან წამოღებული წიგნების, კომიქსებისა და მანგების შესახებ ინფორმაციის ერთ სივრცეში განთავსებას.

პროგრამა დაწერილია Flask ფრეიმვორქზე. ამ შემთხვევაში, მხოლოდ ერთი საიტიდან, Parsek1-დან წამოვიღე კომიქსების შესახებ ინფორმაცია, პარსინგის საშუალებით. სანამ მომხმარებელი ინფორმაციაზე მიიღებს წვდომას, საიტზე უნდა გაიაროს რეგისტრაცია/ავტორიზაცია. სარეგისტრაციო ფორმაში პაროლების დასაშიფრად გამოვიყენე Werkzeug ბიბლიოთეკა, მონაცემების შესანახად - SQLite მონაცემთა ბაზა, ხოლო მონაცემებთან სამუშაოდ - SQLAlchemy. 
