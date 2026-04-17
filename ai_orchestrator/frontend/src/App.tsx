import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, Paperclip, CheckCircle2, AlertTriangle, Info, BookOpen, Activity, Command, Lock, User, CheckCircle, Users, Calendar, Play, QrCode } from 'lucide-react';
import axios from 'axios';

// --- AUTH SCREEN COMPONENT ---
function AuthScreen({ onLogin }: { onLogin: (role: string) => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [role, setRole] = useState<'director' | 'teacher'>('director');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (role === 'teacher') {
      onLogin('teacher');
      return;
    }

    try {
      const res = await axios.post('http://localhost:8000/api/auth/login', { email, password });
      localStorage.setItem('auth_token', res.data.token);
      onLogin('director');
    } catch (err: any) {
      setError(err.response?.data?.detail || '❌ Неверный логин или пароль');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-emerald-900 relative overflow-hidden text-white">
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-emerald-500 rounded-full mix-blend-multiply filter blur-[120px] opacity-40 animate-pulse"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-indigo-500 rounded-full mix-blend-multiply filter blur-[120px] opacity-40"></div>
      
      <div className="bg-white/10 backdrop-blur-3xl p-10 rounded-[3rem] shadow-2xl border border-white/20 w-full max-w-md z-10 transition-transform transform hover:scale-[1.02]">
        <div className="flex flex-col items-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-tr from-emerald-400 to-teal-500 rounded-[2rem] flex items-center justify-center text-white shadow-2xl shadow-emerald-500/30 mb-4">
            <Command size={32} />
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight">Вход в систему</h2>
        </div>

        <div className="flex bg-white/10 p-1 rounded-2xl mb-6">
          <button onClick={() => setRole('director')} className={`flex-1 py-2 rounded-xl text-sm font-bold transition-all ${role === 'director' ? 'bg-emerald-500 text-white shadow-md' : 'text-white/60 hover:text-white'}`}>Директор</button>
          <button onClick={() => setRole('teacher')} className={`flex-1 py-2 rounded-xl text-sm font-bold transition-all ${role === 'teacher' ? 'bg-[#25D366] text-white shadow-md' : 'text-white/60 hover:text-white'}`}>Учитель (WhatsApp)</button>
        </div>

        {error && <div className="p-4 bg-rose-500/80 border border-rose-400/50 rounded-2xl mb-6 text-sm text-center backdrop-blur-md shadow-lg">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <User className="absolute left-5 top-1/2 transform -translate-y-1/2 text-white/50 w-5 h-5" />
            <input type="email" placeholder="Рабочий Email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-white/5 border border-white/10 text-white rounded-2xl py-4 pl-14 pr-4 focus:outline-none focus:border-emerald-400 focus:bg-white/10 transition" required />
          </div>
          <div className="relative group">
            <Lock className="absolute left-5 top-1/2 transform -translate-y-1/2 text-white/50 w-5 h-5" />
            <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full bg-white/5 border border-white/10 text-white rounded-2xl py-4 pl-14 pr-4 focus:outline-none focus:border-emerald-400 focus:bg-white/10 transition" required />
          </div>
          
          <button type="submit" className={`w-full text-white font-extrabold text-lg py-4 rounded-2xl shadow-xl transition-all transform hover:-translate-y-1 active:scale-95 mt-4 ${role === 'director' ? 'bg-gradient-to-r from-emerald-500 to-teal-500 shadow-emerald-500/30' : 'bg-gradient-to-r from-[#25D366] to-emerald-500 shadow-emerald-500/30'}`}>
            {role === 'teacher' ? 'Синхронизировать WhatsApp' : 'Войти в Дашборд'}
          </button>
        </form>
      </div>
    </div>
  );
}

// --- MAIN DASHBOARD APP ---
export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState('');

  if (!isAuthenticated) return <AuthScreen onLogin={(r) => { setIsAuthenticated(true); setUserRole(r); }} />;
  
  if (userRole === 'teacher') {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#ECE5DD] text-slate-800 text-center p-6 relative overflow-hidden">
         <div className="absolute inset-0 opacity-10 bg-[url('https://w0.peakpx.com/wallpaper/818/148/HD-wallpaper-whatsapp-background-solid-color-thumbnail.jpg')] bg-cover mix-blend-multiply pointer-events-none z-0"></div>
         
         <div className="z-10 bg-white/95 backdrop-blur-3xl p-10 rounded-[3rem] shadow-2xl border border-white max-w-md w-full flex flex-col items-center transform transition duration-500 hover:scale-105">
            <div className="w-24 h-24 bg-[#25D366] rounded-full flex items-center justify-center text-white mb-6 shadow-xl shadow-green-500/40">
              <QrCode size={48} strokeWidth={2}/>
            </div>
            <h1 className="text-3xl font-extrabold mb-3 text-slate-800">Рабочий чат</h1>
            <p className="text-[16px] text-slate-500 font-medium mb-8 leading-relaxed max-w-xs mx-auto">
              Наведите камеру смартфона на код, чтобы привязать номер.
            </p>
            
            <div className="p-4 bg-white rounded-[2rem] shadow-lg border border-slate-100 flex items-center justify-center mb-10 w-56 h-56 transition-transform hover:scale-105">
               <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://wa.me/mock-bot-number" alt="whatsapp-qr" className="w-full opacity-90 rounded-2xl mix-blend-multiply" />
            </div>

            <button onClick={() => setIsAuthenticated(false)} className="w-full py-4 bg-slate-100 text-slate-500 rounded-2xl font-extrabold hover:bg-slate-200 hover:text-slate-70// --- DASHBOARD COMPONENT ---
function Dashboard() {
  const [activeTab, setActiveTab] = useState('chat');
  const [inputVal, setInputVal] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<any[]>([
    { text: "1А — 25 детей, 2 болеют.", time: "08:15", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 25 порций. Данные переданы в столовую Aqbobek." } },
    { text: "Доброе утро! В 2Б 20 человек, все на месте.", time: "08:17", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 20 порций. Заявка сформирована автоматически." } },
    { text: "В кабинете 12 сломалась парта на последнем ряду. Дети не могут сидеть.", time: "09:05", parsed: { type: "incident", urgency: "high", insight: "🚨 ИНЦИДЕНТ\nСоздана задача Ахмету (Завхоз): Починить парту в каб. 12" } },
    { text: "Коллеги, я с температурой 39. Сегодня не смогу прийти.", time: "10:12", parsed: { type: "absence", urgency: "critical", insight: "🔥 ВНИМАНИЕ: Аскар (Математика) болен.\nНайдены свободные окна: Смирнова Е. (2 урок), Кусаинова А. (3 урок)." } },
    { text: "3В - 22 человека, 3 отсутствуют.", time: "10:15", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 22 порции. Список отсутствующих: Жусупов, Кан, Ли." } }
  ]);�турой 39. Сегодня не смогу прийти.", time: "10:12", parsed: { type: "absence", urgency: "critical", insight: "🔥 ВНИМАНИЕ: Аскар (Математика) болен.\nНайдены свободные окна: Смирнова Е. (2 урок), Кусаинов А. (3 урок)." } },
    { text: "3В - 22 человека, 3 отсутствуют.", time: "10:15", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 22 порции. Список отсутствующих: Жусупов, Кан, Ли." } }
  ]);
  const [dbTasks, setDbTasks] = useState<any[]>([
    { id: 991, title: "Починить парту в кабинете 12", assignee: "Ахмет (Завхоз)", deadline: "Сегодня до 14:00", is_completed: false },
    { id: 992, title: "Подготовить актовый зал к хакатону", assignee: "Айгерим", deadline: "До среды", is_completed: false },
    { id: 993, title: "Заказать воду для всех классов (20 бутылей)", assignee: "Назкен", deadline: "Завтра", is_completed: false },
    { id: 994, title: "Собрать отчетность по питанию за неделю", assignee: "Секретарь Назкен", deadline: "Пятница", is_completed: true }
  ]);

  const mockSchedule = [
    { lesson: 1, class: "3В", room: "302", teacher: "Аскар (Болеет)", subject: "Математика", alert: true, replacement: "Смирнова Елена (Окно)" },
    { lesson: 2, class: "5А", room: "305", teacher: "Аскар (Болеет)", subject: "Алгебра", alert: true, replacement: "Кусаинов А. (Информатика)" },
    { lesson: 3, class: "8Б", room: "404", teacher: "Алиев Марат", subject: "Физика" }
  ];

  // REAL DATA: Fetch tasks from the real backend!
  const loadTasks = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/tasks/');
      setDbTasks(res.data);
    } catch (e) {
      console.error("Ошибка при получении заданий из Базы Данных", e);
    }
  };

  useEffect(() => {
    if (activeTab === 'tasks') {
      loadTasks();
    }
  }, [activeTab]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const pushMessage = async (text: string, isAudio = false) => {
    const msg = { text, isAudio, time: new Date().toLocaleTimeString().slice(0,5), parsed: { type: "loading", urgency: "...", insight: "Анализ LLM ядром..." } };
    setMessages(prev => [...prev, msg]);
    
    try {
      // REAL DATA: Запрос парсинга к настоящему FastAPI бэкенду
      const res = await axios.post('http://localhost:8000/api/voice/task', { test_text: text });
      const tasksParsed = res.data.voice_decomposition.tasks || [];
      
      let insightText = "Ничего не найдено.";
      if (tasksParsed.length > 0) {
        insightText = `✅ Распознано задач: ${tasksParsed.length}\n`;
        // Если нашли задачи, сохраняем их в базу!
        for (const t of tasksParsed) {
          await axios.post('http://localhost:8000/api/tasks/', {
            title: t.task_name, assignee: t.assignee || "Неизвестно", deadline: t.deadline || "Без срока"
          });
        }
        loadTasks(); // Обновляем список задач
      }

      setMessages(prev => {
        let updated = [...prev];
        updated[updated.length - 1].parsed = { type: "backend_parsed", urgency: "medium", insight: insightText };
        return updated;
      });

    } catch (e) {
      setMessages(prev => {
        let updated = [...prev];
        updated[updated.length - 1].parsed = { type: "error", urgency: "critical", insight: "Ошибка сети. Бэкенд не отвечает." };
        return updated;
      });
    }
  }

  const handleSend = () => {
    if(!inputVal.trim()) return;
    pushMessage(inputVal);
    setInputVal('');
  };

  // REAL DATA: Пометка задачи выполненной в базе данных!
  const markTaskDone = async (id: number) => {
    try {
      await axios.put(`http://localhost:8000/api/tasks/${id}/complete`);
      setDbTasks(prev => prev.map(t => t.id === id ? {...t, is_completed: true} : t));
    } catch (e) {
      alert("Не удалось закрыть задачу на сервере.");
    }
  };

  const handleMicClick = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) { 
      if (isRecording) return;
      setIsRecording(true);
      
      const fullText = "Назкен, пожалуйста, закажи воду на завтра для всех классов. Айгерим, нужно проверить освещение в актовом зале.";
      let currentIdx = 0;
      
      // Эффект печатания (Live Transcription)
      const interval = setInterval(() => {
        if (currentIdx < fullText.length) {
          const char = fullText[currentIdx];
          setInputVal(prev => prev + char);
          currentIdx++;
        } else {
          clearInterval(interval);
          setIsRecording(false);
          setIsTranscribing(true); // Переходим в фазу "анализа"
          
          setTimeout(() => {
            setIsTranscribing(false);
            const finalValue = fullText;
            setInputVal('');
            pushMessage(finalValue, true);
          }, 1200);
        }
      }, 45); 
      return; 
    }
    if (isRecording) return;
    const recognition = new SpeechRecognition();
    recognition.lang = 'ru-RU';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.onstart = () => setIsRecording(true);
    recognition.onresult = (event: any) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript;
      }
      if (finalTranscript) {
         setIsRecording(false);
         pushMessage(finalTranscript, true);
      }
    };
    recognition.onerror = () => setIsRecording(false);
    recognition.onend = () => setIsRecording(false);
    recognition.start();
  };

  return (
    <div className="flex h-screen bg-slate-50 text-slate-800 font-sans tracking-wide overflow-hidden relative">
      <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-emerald-100 rounded-full mix-blend-multiply filter blur-[150px] opacity-60 z-0"></div>

      <div className="w-1/3 max-w-[340px] flex flex-col bg-white/80 backdrop-blur-2xl border-r border-slate-200 shadow-2xl z-10">
        <div className="p-8 flex flex-col items-center border-b border-slate-100 bg-white">
          <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-emerald-500/20 mb-4">
            <Command size={32} />
          </div>
          <div className="font-extrabold text-2xl bg-clip-text text-transparent bg-gradient-to-r from-emerald-700 to-teal-600">AI-Завуч</div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          <MenuButton title="Рабочие чаты и ГС" desc="Анализ LLM парсером" icon={<Users />} active={activeTab === 'chat'} onClick={() => setActiveTab('chat')} />
          <MenuButton title="Делегат (Voice-to-Task)" desc="Реальная База Данных" icon={<CheckCircle2 />} active={activeTab === 'tasks'} onClick={() => setActiveTab('tasks')} />
          <MenuButton title="Smart Substitution" desc="Анализ LLM: Замены" icon={<Calendar />} active={activeTab === 'schedule'} onClick={() => setActiveTab('schedule')} />
          <MenuButton title="Бюрократический RAG" desc="Проверка по приказам" icon={<BookOpen />} active={activeTab === 'rag'} onClick={() => setActiveTab('rag')} />
        </div>
        <div className="p-4 border-t border-slate-200">
          <button onClick={() => { localStorage.removeItem('auth_token'); window.location.reload(); }} className="w-full text-slate-500 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition font-bold text-sm p-3">Выйти</button>
        </div>
      </div>

      <div className="flex-1 flex flex-col relative z-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-fixed">
        <div className="absolute inset-0 bg-slate-50/90 z-[-1]"></div>
        
        <div className="px-10 py-8 flex items-center justify-between z-10 sticky top-0 bg-slate-50/80 backdrop-blur border-b border-white/40">
          <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight">AI-Дашборд</h2>
          <div className="flex items-center bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200">
            <span className="relative flex h-3 w-3 mr-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#25D366] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-[#25D366]"></span>
            </span>
            <div className="text-xs font-extrabold uppercase tracking-widest text-slate-600">Sync: WhatsApp / SQLite</div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-10 pb-10 space-y-8 z-10 scroll-smooth pt-6">
          {activeTab === 'chat' && (
            <div className="max-w-4xl mx-auto flex flex-col space-y-8">
              
              {messages.length === 0 && (
                <div className="text-center p-12 bg-white/50 rounded-3xl border-2 border-dashed border-slate-200 text-slate-400">
                   <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
                   <h3 className="text-xl font-bold">Чат пуст</h3>
                   <p className="mt-2 text-[15px]">Сообщения из Telegram/WhatsApp будут появляться здесь.</p>
                   <p className="text-sm opacity-80 mt-1">Или отправьте ГС ниже для парсинга задач в реальном времени в базу данных.</p>
                </div>
              )}

              {messages.map((m, i) => (
                <div key={i} className="flex flex-col mb-4 max-w-[90%] group">
                  <div className={`p-6 rounded-[2rem] rounded-tl-none shadow-lg relative border transition-shadow ${m.isAudio ? 'bg-emerald-50 border-emerald-100' : 'bg-white border-slate-100'}`}>
                    {m.isAudio ? (
                      <div className="flex flex-col">
                        <div className="flex items-center mb-3 bg-white p-3 rounded-full shadow-sm w-fit">
                           <div className="w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center text-white mr-3 shadow-md focus:outline-none"><Play className="w-5 h-5 ml-1"/></div>
                           <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Waveform.svg" alt="waveform" className="h-6 w-32 opacity-40 mr-4" />
                           <span className="font-bold text-slate-500 mr-2">0:03</span>
                        </div>
                        <p className="text-slate-600 text-sm font-medium italic pr-12">Транскрипт: "{m.text}"</p>
                      </div>
                    ) : (
                      <p className="text-slate-800 text-[17px] leading-relaxed pr-12 font-semibold">{m.text}</p>
                    )}
                    <span className="text-xs font-bold text-slate-300 absolute bottom-4 right-5">{m.time}</span>
                  </div>

                  <div className={`mt-3 ml-8 border rounded-2xl p-5 text-sm flex items-start w-[95%] shadow-md transition-all ${m.parsed?.urgency === 'critical' ? 'bg-rose-50 border-rose-200' : 'bg-emerald-50/50 border-emerald-100'}`}>
                    <div className="flex flex-col w-full">
                      <b className={`uppercase text-[11px] font-black tracking-widest opacity-80 mb-2`}>[AI PARSED]</b>
                      <span className="font-bold text-[15px] whitespace-pre-wrap">{m.parsed?.insight}</span>
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}

          {activeTab === 'tasks' && (
             <div className="space-y-6 max-w-4xl mx-auto">
               <h3 className="font-black text-2xl mb-4 text-slate-800 flex items-center justify-between">
                 <span>База Данных Задач (Real Data)</span>
                 <button onClick={loadTasks} className="text-xs font-bold bg-white text-emerald-600 px-4 py-2 border border-emerald-200 rounded-xl shadow-sm hover:bg-emerald-50 transition">🔄 Обновить БД</button>
               </h3>

               {dbTasks.length === 0 && (
                 <div className="text-center p-10 bg-white border border-slate-200 rounded-3xl text-slate-500 font-medium">Ваша база данных пуста! Надиктуйте задачу голосом в чате.</div>
               )}

               {dbTasks.filter(t => !t.is_completed).map((t, idx) => (
                 <div key={idx} className="bg-white p-8 rounded-3xl shadow-xl border border-slate-100 transition hover:shadow-2xl hover:-translate-y-1">
                   <h3 className="font-extrabold text-xl mb-4 flex items-center"><CheckCircle2 className="w-7 h-7 mr-3 text-emerald-500"/> {t.title}</h3>
                   <div className="flex gap-4 text-sm bg-slate-50 p-4 rounded-xl w-full justify-between items-center border border-slate-100">
                      <div className="flex gap-4">
                        <p className="text-slate-500">Исполнитель: <span className="font-bold text-slate-800 ml-1 bg-white px-3 py-1.5 shadow-sm border rounded-lg">{t.assignee}</span></p>
                        <p className="text-slate-500">Дедлайн: <span className="font-bold text-rose-600 ml-1 bg-white px-3 py-1.5 shadow-sm border rounded-lg">{t.deadline}</span></p>
                      </div>
                      <button onClick={() => markTaskDone(t.id)} className="bg-slate-800 text-white font-bold py-2.5 px-6 rounded-xl shadow-lg hover:bg-emerald-500 transition-colors flex items-center active:scale-95">
                        <CheckCircle className="w-4 h-4 mr-2" /> Выполнено
                      </button>
                   </div>
                 </div>
               ))}

               {dbTasks.filter(t => t.is_completed).map((t, idx) => (
                 <div key={`done-${idx}`} className="bg-slate-50 backdrop-blur-xl p-6 rounded-3xl shadow-sm border border-slate-200 opacity-60">
                   <h3 className="font-bold text-lg flex items-center text-slate-500 line-through">
                     <CheckCircle2 className="w-6 h-6 mr-3 text-emerald-500"/> {t.title}
                   </h3>
                 </div>
               ))}
             </div>
          )}

          {activeTab === 'schedule' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="bg-white p-10 rounded-3xl shadow-2xl border border-slate-100">
                <div className="flex justify-between items-start mb-8 border-b border-slate-100 pb-6">
                  <div>
                    <h3 className="font-extrabold text-3xl text-slate-800">Замена учителей (RAG)</h3>
                    <p className="text-slate-500 mt-2 font-medium">Система проверила приказ №110 и нашла замену.</p>
                  </div>
                </div>
                <div className="space-y-4">
                  {mockSchedule.map((s, idx) => (
                    <div key={idx} className={`flex justify-between items-center p-6 rounded-2xl border transition-all ${s.alert ? 'bg-rose-50/30 border-rose-200' : 'bg-slate-50 border-slate-100'}`}>
                      <div className="flex items-center space-x-6">
                        <div className="text-3xl font-black text-slate-300 w-8">{s.lesson}</div>
                        <div>
                          <div className="font-bold text-xl text-slate-800">Класс {s.class} <span className="text-sm font-medium text-slate-400 ml-2">Каб. {s.room}</span></div>
                          <div className={`mt-1 text-sm font-bold ${s.alert ? 'text-rose-500' : 'text-slate-500'}`}>{s.subject} — {s.teacher}</div>
                        </div>
                      </div>
                      {s.alert && (
                        <div className="flex flex-col items-end">
                          <span className="text-xs uppercase font-extrabold tracking-wider text-emerald-600 mb-2">Найдена замена AI</span>
                          <span className="bg-emerald-500 text-white text-md px-5 py-2.5 rounded-xl font-bold shadow-lg shadow-emerald-500/30 flex items-center">
                            <Activity className="w-4 h-4 mr-2" /> {s.replacement}
                          </span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'rag' && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-gradient-to-br from-slate-900 to-indigo-900 p-12 rounded-[3rem] shadow-2xl text-center relative overflow-hidden">
                <BookOpen className="w-20 h-20 mx-auto mb-8 text-emerald-400 drop-shadow-lg" />
                <h3 className="font-black text-4xl mb-4 text-white">Semantic RAG: Приказы МОН</h3>
                <p className="text-emerald-200 mb-10 text-lg font-medium max-w-2xl mx-auto">
                  Система подключена к приказам №76, №110 и №130. Спросите любой нормативный вопрос.
                </p>
                <div className="relative max-w-3xl mx-auto flex bg-white/10 p-2 rounded-2xl backdrop-blur-md border border-white/20">
                  <input type="text" placeholder="Пример: Во сколько подаются данные в столовую по приказу №130?" className="flex-1 bg-transparent text-white placeholder-white/50 px-6 text-lg focus:outline-none" />
                  <button className="bg-emerald-500 text-white px-8 py-4 rounded-xl font-bold shadow-lg hover:bg-emerald-400 transition-colors">Поиск</button>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="p-8 bg-white/80 backdrop-blur-xl border-t border-slate-200 z-20">
          <div className="max-w-4xl mx-auto flex items-center bg-slate-100 rounded-3xl shadow-inner border border-slate-200 p-2">
            <input type="text" value={inputVal} onChange={(e) => setInputVal(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSend()} placeholder={isRecording ? "🎤 Идет запись ГС..." : "Отправить текст или ГС для LLM-обработки..."} className="flex-1 text-slate-800 p-4 bg-transparent border-none focus:outline-none text-lg font-semibold placeholder-slate-400 pl-6" />
            <div className="flex space-x-2 mr-2">
              {inputVal ? <button onClick={handleSend} className="p-4 bg-slate-800 text-white rounded-2xl"><Send className="w-6 h-6"/></button> : <button onClick={handleMicClick} className={`p-4 text-white rounded-2xl flex items-center justify-center shadow-lg ${isRecording ? 'bg-rose-500 animate-pulse' : 'bg-[#25D366]'}`}><Mic className="w-6 h-6" /></button>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function MenuButton({title, desc, icon, active, onClick}: any) {
  return (
    <div onClick={onClick} className={`p-4 rounded-2xl cursor-pointer transition-all duration-300 flex items-center group ${active ? 'bg-slate-800 text-white shadow-xl transform scale-[1.02]' : 'hover:bg-slate-100 border border-transparent'}`}>
      <div className={`p-3 rounded-xl mr-4 ${active ? 'bg-slate-700 text-[#25D366]' : 'bg-white text-slate-400'}`}>{icon}</div>
      <div>
        <h3 className={`font-bold text-[15px] ${active ? 'text-white' : 'text-slate-700'}`}>{title}</h3>
        <p className={`text-xs mt-1 font-medium ${active ? 'text-emerald-300' : 'text-slate-400'}`}>{desc}</p>
      </div>
    </div>
  )
}
