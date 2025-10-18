import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import Icon from '@/components/ui/icon';

const Index = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    question1: '',
    question2: '',
    question3: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.firstName || !formData.lastName) {
      toast({
        title: "Ошибка",
        description: "Пожалуйста, заполните имя и фамилию",
        variant: "destructive"
      });
      return;
    }

    if (!formData.question1 || !formData.question2 || !formData.question3) {
      toast({
        title: "Ошибка", 
        description: "Пожалуйста, ответьте на все вопросы",
        variant: "destructive"
      });
      return;
    }

    toast({
      title: "Успешно!",
      description: "Ваши ответы отправлены"
    });

    setFormData({
      firstName: '',
      lastName: '',
      question1: '',
      question2: '',
      question3: ''
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl p-8 md:p-12 shadow-lg animate-fade-in">
        <div className="mb-8 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full mb-4">
            <Icon name="ClipboardList" size={32} className="text-primary" />
          </div>
          <h1 className="text-3xl md:text-4xl font-light text-gray-900 mb-2">
            Тестовая форма
          </h1>
          <p className="text-gray-600">Пожалуйста, заполните все поля формы</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="space-y-6 pb-6 border-b border-gray-200">
            <h2 className="text-xl font-medium text-gray-900 flex items-center gap-2">
              <Icon name="User" size={20} className="text-primary" />
              Личная информация
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="firstName" className="text-gray-700">
                  Имя
                </Label>
                <Input
                  id="firstName"
                  value={formData.firstName}
                  onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                  placeholder="Введите ваше имя"
                  className="transition-all focus:scale-[1.02]"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="lastName" className="text-gray-700">
                  Фамилия
                </Label>
                <Input
                  id="lastName"
                  value={formData.lastName}
                  onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                  placeholder="Введите вашу фамилию"
                  className="transition-all focus:scale-[1.02]"
                />
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <h2 className="text-xl font-medium text-gray-900 flex items-center gap-2">
              <Icon name="HelpCircle" size={20} className="text-primary" />
              Тестовые вопросы
            </h2>

            <div className="space-y-4">
              <Label className="text-gray-900 font-medium">
                1. Как вы оцениваете качество сервиса?
              </Label>
              <RadioGroup
                value={formData.question1}
                onValueChange={(value) => setFormData({ ...formData, question1: value })}
                className="space-y-3"
              >
                {['Отлично', 'Хорошо', 'Удовлетворительно', 'Плохо'].map((option) => (
                  <div key={option} className="flex items-center space-x-3 hover:bg-gray-50 p-2 rounded-md transition-colors">
                    <RadioGroupItem value={option} id={`q1-${option}`} />
                    <Label htmlFor={`q1-${option}`} className="cursor-pointer flex-1 font-normal">
                      {option}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>

            <div className="space-y-4">
              <Label className="text-gray-900 font-medium">
                2. Что вам понравилось больше всего?
              </Label>
              <RadioGroup
                value={formData.question2}
                onValueChange={(value) => setFormData({ ...formData, question2: value })}
                className="space-y-3"
              >
                {['Дизайн', 'Функциональность', 'Скорость работы', 'Простота использования'].map((option) => (
                  <div key={option} className="flex items-center space-x-3 hover:bg-gray-50 p-2 rounded-md transition-colors">
                    <RadioGroupItem value={option} id={`q2-${option}`} />
                    <Label htmlFor={`q2-${option}`} className="cursor-pointer flex-1 font-normal">
                      {option}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>

            <div className="space-y-4">
              <Label htmlFor="question3" className="text-gray-900 font-medium">
                3. Дополнительные комментарии или предложения
              </Label>
              <Textarea
                id="question3"
                value={formData.question3}
                onChange={(e) => setFormData({ ...formData, question3: e.target.value })}
                placeholder="Поделитесь вашими мыслями..."
                rows={4}
                className="resize-none transition-all focus:scale-[1.01]"
              />
            </div>
          </div>

          <Button 
            type="submit" 
            className="w-full h-12 text-base font-medium shadow-md hover:shadow-lg transition-all hover:scale-[1.02]"
          >
            <Icon name="Send" size={18} className="mr-2" />
            Отправить ответы
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default Index;
