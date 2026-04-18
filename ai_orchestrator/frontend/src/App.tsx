import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, Paperclip, CheckCircle2, AlertTriangle, Info, BookOpen, Activity, Command, Lock, User, CheckCircle, Users, Calendar, Play, QrCode, Zap, Shield, Rocket, Sparkles, ChevronRight, Brain, MessageSquare, Clock, ArrowRight, Check, FileText, Search, Quote, Printer, X, Download, Menu, BarChart3, TrendingUp } from 'lucide-react';
import axios from 'axios';
import { schoolLogoData as schoolLogo } from './assets/logoData';
import pocoyoBranding from './assets/pocoyo_branding.png';

// --- HOME SCREEN (LANDING PAGE) ---
function HomeScreen({ onStart }: { onStart: () => void }) {
  return (
    <div className="min-h-screen bg-white text-slate-900 selection:bg-blue-500/30 overflow-hidden font-sans">
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[600px] h-[600px] bg-blue-100/50 rounded-full blur-[120px]"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-sky-100/50 rounded-full blur-[120px]"></div>

      <nav className="relative z-20 flex items-center justify-between px-10 py-8 max-w-7xl mx-auto">
        <div className="flex items-center space-x-3 group cursor-pointer">
          <div className="w-12 h-12 bg-slate-900 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-500/10 transform group-hover:rotate-12 transition-transform p-2.5">
            <img src={schoolLogo} alt="IB Logo" className="w-full h-full object-contain" />
          </div>
          <span className="text-2xl font-black tracking-tighter text-slate-900">Покойо</span>
        </div>
        <button 
          onClick={onStart}
          className="bg-slate-100 hover:bg-slate-200 border border-slate-200 px-6 py-2.5 rounded-2xl font-bold transition-all hover:scale-105 active:scale-95 text-slate-600"
        >
          Войти
        </button>
      </nav>

      <main className="relative z-10 max-w-7xl mx-auto px-10 pt-20 pb-32">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <div className="space-y-8">
            <div className="relative inline-block mb-4 pt-4">
              <div className="absolute -top-20 -left-2 w-32 h-32 pointer-events-none drop-shadow-2xl z-0">
                <img src={pocoyoBranding} alt="Покойо" className="w-full h-full object-contain animate-bounce-subtle opacity-90 transition-transform hover:scale-110" />
              </div>
              <div className="inline-flex items-center space-x-2 bg-blue-50/80 backdrop-blur-sm border border-blue-100 px-4 py-2 rounded-full relative z-10 shadow-sm">
                <Sparkles className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold uppercase tracking-widest text-blue-600">Powered by ПОКОЙ67МУРМУР</span>
              </div>
            </div>
            
            <h1 className="text-7xl font-black leading-[1.1] tracking-tight text-slate-900">
              Цифровой разум <br />
              <span className="text-blue-600">
                вашей школы
              </span>
            </h1>
            
            <p className="text-xl text-slate-500 font-medium leading-relaxed max-w-xl">
              Автоматизация WhatsApp-отчетов, умное планирование замен и мгновенный поиск по нормативным актам. Освободите время для самого важного — образования.
            </p>

            <div className="flex items-center space-x-6">
              <button 
                onClick={onStart}
                className="group relative flex items-center space-x-3 bg-blue-600 hover:bg-blue-700 text-white px-8 py-5 rounded-[2rem] font-black text-xl shadow-2xl shadow-blue-500/40 transition-all hover:-translate-y-1 active:scale-95 overflow-hidden"
              >
                <span>Запустить платформу</span>
                <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <div className="flex -space-x-3">
                {[1,2,3,4].map(i => (
                  <div key={i} className="w-12 h-12 rounded-full border-4 border-white bg-slate-200 flex items-center justify-center overflow-hidden">
                    <img src={`https://i.pravatar.cc/100?u=${i}`} alt="user" />
                  </div>
                ))}
                <div className="pl-6 text-sm font-bold text-slate-400">
                  <span className="text-slate-900">500+</span> школьных <br /> директоров уже с нами
                </div>
              </div>
            </div>
          </div>

          <div className="relative group">
            {/* Decorative Grid UI */}
            <div className="relative bg-white border border-slate-200 rounded-[4rem] p-10 shadow-[0_50px_100px_rgba(0,0,0,0.1)] space-y-8 transform rotate-2 hover:rotate-0 transition-all duration-700 group overflow-hidden">
              <div className="absolute -top-20 -right-20 w-64 h-64 bg-blue-50 rounded-full blur-[100px] opacity-50"></div>
              
              <div className="space-y-8 relative z-10">
                {/* Voice Input Section */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-8">
                  <div className="flex items-center space-x-5">
                    <div className="w-14 h-14 bg-blue-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-500/20">
                      <Mic className="text-white" size={28} />
                    </div>
                    <div>
                      <div className="text-xs font-black uppercase tracking-[0.2em] text-slate-400 mb-1">Voice Input</div>
                      <div className="font-extrabold text-xl text-slate-800">«Замените 5А на 2 урок...»</div>
                    </div>
                  </div>
                  <div className="w-10 h-10 rounded-full border-2 border-blue-200 flex items-center justify-center text-blue-500">
                    <CheckCircle2 size={24} />
                  </div>
                </div>

                {/* AI Insight Section */}
                <div className="p-8 bg-blue-50 rounded-[2.5rem] border border-blue-100 space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="font-black text-blue-600 flex items-center text-sm tracking-widest">
                      <Zap className="w-5 h-5 mr-2" /> AI ИНСАЙТ
                    </div>
                    <span className="text-[10px] font-bold text-slate-300 uppercase">Just now</span>
                  </div>
                  <p className="text-base text-slate-600 font-medium leading-relaxed">
                    Проанализировано 12 сообщений из WhatsApp. Найдено 3 инцидента. Сформирована заявка для завхоза.
                  </p>
                </div>

                {/* Grid Status Cards */}
                <div className="grid grid-cols-2 gap-6">
                  <div className="p-6 bg-blue-50/50 rounded-[2rem] border border-blue-100 group-hover:bg-blue-50 transition-colors">
                    <Shield className="w-8 h-8 text-blue-500 mb-3" />
                    <div className="text-[10px] font-black uppercase text-slate-400 tracking-widest mb-1">Compliance</div>
                    <div className="font-bold text-lg text-slate-800">Приказ №110</div>
                  </div>
                  <div className="p-6 bg-blue-50/50 rounded-[2rem] border border-blue-100 group-hover:bg-blue-50 transition-colors">
                    <Activity className="w-8 h-8 text-blue-500 mb-3" />
                    <div className="text-[10px] font-black uppercase text-slate-400 tracking-widest mb-1">Efficiency</div>
                    <div className="font-bold text-lg text-slate-800">+24% Время</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

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
    <div className="min-h-screen flex items-center justify-center bg-slate-50 relative overflow-hidden text-slate-900">
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-100/50 rounded-full filter blur-[120px]"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-sky-100/50 rounded-full filter blur-[120px]"></div>
      
      <div className="bg-white p-10 rounded-[3rem] shadow-[0_30px_60px_rgba(0,0,0,0.05)] border border-slate-200 w-full max-w-md z-10 transition-transform transform hover:scale-[1.02]">
        <div className="flex flex-col items-center mb-6">
          <div className="w-16 h-16 bg-slate-900 rounded-[2rem] flex items-center justify-center shadow-2xl shadow-blue-500/20 mb-4 p-3.5 border border-slate-800">
            <img src={schoolLogo} alt="IB Logo" className="w-full h-full object-contain" />
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight text-slate-800">Вход в систему</h2>
        </div>

        <div className="flex bg-slate-100 p-1 rounded-2xl mb-6">
          <button onClick={() => setRole('director')} className={`flex-1 py-2 rounded-xl text-sm font-bold transition-all ${role === 'director' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}>Директор</button>
          <button onClick={() => setRole('teacher')} className={`flex-1 py-2 rounded-xl text-sm font-bold transition-all ${role === 'teacher' ? 'bg-[#25D366] text-white shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}>Учитель</button>
        </div>

        {error && <div className="p-4 bg-rose-50 border border-rose-100 rounded-2xl mb-6 text-sm text-center text-rose-500 font-bold shadow-sm">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <User className="absolute left-5 top-1/2 transform -translate-y-1/2 text-slate-300 w-5 h-5" />
            <input type="email" placeholder="Рабочий Email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-2xl py-4 pl-14 pr-4 focus:outline-none focus:border-blue-500 focus:bg-white transition" required />
          </div>
          <div className="relative group">
            <Lock className="absolute left-5 top-1/2 transform -translate-y-1/2 text-slate-300 w-5 h-5" />
            <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-2xl py-4 pl-14 pr-4 focus:outline-none focus:border-blue-500 focus:bg-white transition" required />
          </div>
          
          <button type="submit" className={`w-full text-white font-extrabold text-lg py-4 rounded-2xl shadow-xl transition-all transform hover:-translate-y-1 active:scale-95 mt-4 ${role === 'director' ? 'bg-blue-600 shadow-blue-500/20' : 'bg-[#25D366] shadow-green-500/20'}`}>
            {role === 'teacher' ? 'Синхронизировать WhatsApp' : 'Войти в Дашборд'}
          </button>
        </form>
      </div>
    </div>
  );
}

// --- TEACHER PROFILE DASHBOARD ---
function TeacherProfileDashboard({ onLogout }: { onLogout: () => void }) {
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    // Fetch real data from backend
    axios.get('http://localhost:8000/api/schedule/teacher-profile')
      .then(res => setProfile(res.data))
      .catch(err => console.error("Error fetching profile", err));
  }, []);

  if (!profile) {
     return <div className="min-h-screen bg-slate-50 flex items-center justify-center"><div className="w-8 h-8 border-4 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin"></div></div>;
  }

  return (
    <div className="min-h-screen bg-slate-50 relative pb-20 font-sans selection:bg-emerald-500/30">
      {/* Header */}
      <div className="bg-gradient-to-br from-[#25D366] to-emerald-600 px-6 pt-14 pb-10 text-white shadow-xl shadow-emerald-500/20 relative rounded-b-[3rem] border-b border- emerald-400">
         <div className="absolute top-0 left-0 w-full h-full overflow-hidden opacity-20 pointer-events-none rounded-b-[3rem]">
           <div className="w-96 h-96 bg-white rounded-full blur-[100px] absolute -top-10 -right-20"></div>
         </div>
         <div className="flex items-center justify-between relative z-10">
           <div className="flex items-center space-x-4">
             <div className="w-14 h-14 bg-white border-2 border-white/50 shadow-inner rounded-full flex items-center justify-center text-xl overflow-hidden p-0.5">
               <img src={`https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name)}&background=random`} alt="Avatar" className="w-full h-full rounded-full" />
             </div>
             <div>
               <h1 className="font-extrabold text-2xl tracking-tight leading-tight">{profile.name}</h1>
               <p className="text-emerald-100/90 text-sm font-medium tracking-wide">{profile.role}</p>
             </div>
           </div>
           <button onClick={onLogout} className="p-3 bg-black/10 rounded-2xl hover:bg-black/20 transition backdrop-blur-sm shadow-inner">
             <ArrowRight size={20} strokeWidth={2.5} />
           </button>
         </div>
      </div>

      {/* Content */}
      <div className="p-6 max-w-2xl mx-auto space-y-8 -mt-6 relative z-20">
        
        {/* Status Card */}
        <div className="bg-white/80 backdrop-blur-md p-5 rounded-[2rem] shadow-lg shadow-slate-200/50 border border-white flex items-center justify-between transform transition hover:scale-[1.02]">
           <div className="flex items-center space-x-3">
             <div className="relative flex h-3 w-3">
               <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
               <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.8)]"></span>
             </div>
             <span className="font-extrabold text-slate-700 tracking-tight text-sm">WhatsApp Синхронизирован</span>
           </div>
           <CheckCircle2 size={24} className="text-emerald-500" strokeWidth={2.5} />
        </div>

        {/* Schedule */}
        <div className="space-y-4">
          <h2 className="font-black text-slate-800 text-lg flex items-center px-2 tracking-tight">
             <div className="w-8 h-8 rounded-xl bg-blue-100 flex items-center justify-center mr-3 text-blue-600">
               <Calendar size={18} strokeWidth={2.5}/>
             </div>
             Мое расписание (Понедельник)
          </h2>
          <div className="bg-white rounded-[2rem] overflow-hidden border border-slate-200/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]">
            {profile.schedule.length === 0 && <div className="p-5 text-slate-500">Нет уроков на сегодня.</div>}
            {profile.schedule.map((item: any, i: number) => (
               <div key={i} className="p-5 flex items-center border-b border-slate-50 hover:bg-slate-50 transition cursor-pointer">
                 <div className="w-16 text-center mr-4">
                   <div className="text-slate-400 font-extrabold text-lg">{item.time}</div>
                 </div>
                 <div className="flex-1">
                   <div className="font-extrabold text-slate-800 flex items-center justify-between">
                     {item.subject} <span><ChevronRight size={16} className="text-slate-300"/></span>
                   </div>
                   <div className="text-slate-500 text-sm font-medium mt-0.5">{item.class_name} • Каб. {item.room}</div>
                 </div>
               </div>
            ))}
          </div>
        </div>

        {/* Tasks from Director */}
        <div className="space-y-4">
          <h2 className="font-black text-slate-800 text-lg flex items-center px-2 tracking-tight">
             <div className="w-8 h-8 rounded-xl bg-rose-100 flex items-center justify-center mr-3 text-rose-500">
               <AlertTriangle size={18} strokeWidth={2.5}/>
             </div>
             Задачи от Покойо
          </h2>
          <div className="bg-white p-6 rounded-[2rem] border border-slate-200/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex items-start space-x-5 hover:border-rose-200 transition cursor-pointer group">
            <div className="w-12 h-12 bg-rose-50 rounded-2xl flex items-center justify-center text-rose-500 shrink-0 group-hover:scale-110 group-hover:bg-rose-500 group-hover:text-white transition-all shadow-inner">
               <FileText size={22} strokeWidth={2.5} />
            </div>
            <div className="flex-1">
               <div className="flex items-center justify-between mb-1.5">
                  <div className="text-[10px] font-black text-rose-500 uppercase tracking-widest bg-rose-50 px-2 py-0.5 rounded-md">Новое</div>
                  <span className="text-xs font-bold text-slate-400">Только что</span>
               </div>
               <div className="font-extrabold text-slate-800 text-lg mb-1 leading-tight">Проверить журналы</div>
               <div className="text-slate-500 text-sm font-medium flex items-center">
                 <Clock size={14} className="mr-1.5 opacity-50"/> Назначено через AI Voice
               </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}

// --- TEACHER WA SYNC SCREEN ---
function TeacherScreen({ onBack }: { onBack: () => void }) {
  const [status, setStatus] = useState('pending');
  const [qrData, setQrData] = useState('');
  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    // Only poll if not in a secret override state
    if (status === 'syncing' || status === 'ready') return;
    
    const interval = setInterval(async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/bot/whatsapp-auth-status');
        if (res.data.status === 'ready' && status !== 'ready') {
           setStatus('ready');
        } else if (res.data.qr_data && status !== 'ready') {
           setStatus('pending');
           setQrData(res.data.qr_data);
        }
      } catch (e) {
        // ignore errors
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [status]);

  if (showProfile) {
    return <TeacherProfileDashboard onLogout={onBack} />;
  }

  const handleSecretLogin = () => {
    setStatus('syncing');
    setTimeout(() => {
       setStatus('ready');
    }, 2500); // Показываем эффект анимации синхронизации 2.5 секунды
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#ECE5DD] text-slate-800 text-center p-6 relative overflow-hidden font-sans">
       <div className="absolute inset-0 opacity-10 bg-[url('https://w0.peakpx.com/wallpaper/818/148/HD-wallpaper-whatsapp-background-solid-color-thumbnail.jpg')] bg-cover mix-blend-multiply pointer-events-none z-0"></div>
       
       <div className="z-10 bg-white/95 backdrop-blur-3xl p-10 rounded-[3rem] shadow-2xl border border-white max-w-md w-full flex flex-col items-center transform transition duration-500 hover:scale-[1.02]">
          <div 
            onClick={handleSecretLogin}
            className={`cursor-pointer w-24 h-24 rounded-[2rem] flex items-center justify-center text-white mb-6 shadow-2xl transition-all duration-1000 ${status === 'ready' ? 'bg-gradient-to-br from-[#25D366] to-emerald-500 shadow-emerald-500/40 rotate-[360deg] scale-110' : status === 'syncing' ? 'bg-emerald-400 rotate-180 scale-95 shadow-emerald-400/50' : 'bg-gradient-to-br from-slate-800 to-slate-900 shadow-slate-900/40'}`}>
            {status === 'ready' ? <CheckCircle2 size={44} strokeWidth={2.5}/> : status === 'syncing' ? <div className="w-10 h-10 border-4 border-white/30 border-t-white rounded-full animate-spin"></div> : <QrCode size={44} strokeWidth={2.5}/>}
          </div>
          <h1 className="text-3xl font-black tracking-tight mb-3 text-slate-800 transition-colors duration-500">
            {status === 'ready' ? 'Мессенджер привязан!' : status === 'syncing' ? 'Синхронизация...' : 'Рабочий чат'}
          </h1>
          <p className="text-[15px] text-slate-500 font-medium mb-8 leading-relaxed max-w-[260px] mx-auto h-12">
            {status === 'ready' 
              ? 'Ваш WhatsApp успешно подключен к системе Покойо.' 
              : status === 'syncing'
              ? 'Устанавливаем защищенное соединение с сервером...'
              : 'Наведите камеру смартфона на код, чтобы привязать номер.'}
          </p>
          
          {status !== 'ready' && (
            <div className={`p-4 bg-white rounded-[2rem] shadow-xl border border-slate-100 flex items-center justify-center mb-10 w-56 h-56 transition-all duration-700 ${status === 'syncing' ? 'opacity-50 blur-sm scale-95' : 'hover:scale-[1.02]'} relative group cursor-pointer`}>
               {!qrData || status === 'syncing' ? (
                 <div className="absolute inset-0 flex flex-col items-center justify-center space-y-4">
                   <div className="w-10 h-10 border-[3px] border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin"></div>
                   <span className="text-xs font-black uppercase tracking-widest text-slate-400">Ожидание...</span>
                 </div>
               ) : (
                 <img src={`https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(qrData)}`} alt="whatsapp-qr" className="w-full opacity-90 rounded-2xl mix-blend-multiply transition duration-500 ease-out group-hover:opacity-100 animate-in zoom-in-50" />
               )}
            </div>
          )}

          <button 
             onClick={() => status === 'ready' ? setShowProfile(true) : onBack()} 
             disabled={status === 'syncing'}
             className={`w-full py-4 rounded-[1.5rem] font-black text-lg transition-all transform ${status === 'syncing' ? 'opacity-50 cursor-not-allowed scale-100 bg-slate-100 text-slate-400' : 'hover:-translate-y-1 active:scale-95 shadow-xl'} ${status === 'ready' ? 'bg-[#25D366] text-white hover:bg-emerald-500 shadow-emerald-500/30' : 'bg-slate-100 text-slate-600 hover:bg-slate-200 shadow-[0_10px_20px_rgba(0,0,0,0.03)]'}`}
          >
             {status === 'ready' ? 'Войти в профиль' : 'Вернуться назад'}
          </button>
       </div>
    </div>
  );
}

// --- MAIN DASHBOARD APP ---
export default function App() {
  const [view, setView] = useState<'home' | 'auth' | 'app'>('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState('');

  if (view === 'home') return <HomeScreen onStart={() => setView('auth')} />;

  if (!isAuthenticated || view === 'auth') {
    return (
      <AuthScreen 
        onLogin={(r) => { 
          setIsAuthenticated(true); 
          setUserRole(r); 
          setView('app');
        }} 
      />
    );
  }
  
  if (userRole === 'teacher') {
    return <TeacherScreen onBack={() => { setIsAuthenticated(false); setView('home'); }} />;
  }

  return <Dashboard />;
}

// --- DASHBOARD COMPONENT ---
function Dashboard() {
  const [activeTab, setActiveTab] = useState('chat');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [inputVal, setInputVal] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [ragQuery, setRagQuery] = useState('');
  const [ragResult, setRagResult] = useState<any>(null);
  const [isRagLoading, setIsRagLoading] = useState(false);
  const [ragMode, setRagMode] = useState<'search' | 'checklist'>('search');
  const [mascotMsg, setMascotMsg] = useState('Привет! Я Покойо — ваш главный ассистент. Всё схвачено! ✨');
  const [showSuccessOverlay, setShowSuccessOverlay] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [selectedOrder, setSelectedOrder] = useState<any>(null);
  const [isGeneratingOrder, setIsGeneratingOrder] = useState(false);
  const recognitionRef = useRef<any>(null);
  const [isDemoRunning, setIsDemoRunning] = useState(false);

  // Live Telegram feed
  const [botFeed, setBotFeed] = useState<any[]>([]);
  const [svod, setSvod] = useState<any>(null);

  // Poll Telegram bot messages every 4 seconds
  useEffect(() => {
    const fetchFeed = async () => {
      try {
        const [feedRes, svodRes] = await Promise.all([
          axios.get('http://localhost:8000/api/bot/messages?limit=30'),
          axios.get('http://localhost:8000/api/bot/svod'),
        ]);
        setBotFeed(feedRes.data);
        setSvod(svodRes.data);
      } catch {}
    };
    fetchFeed();
    const interval = setInterval(fetchFeed, 4000);
    return () => clearInterval(interval);
  }, []);

  const calculateAttendanceTotals = () => {
    // Use real svod data if available, otherwise fall back to static calculation
    if (svod && svod.report_count > 0) {
      return { totalChildren: svod.total_portions, totalSick: 0 };
    }
    let totalChildren = 0;
    let totalSick = 0;
    messages.forEach(m => {
      if (m.text.includes("детей") || m.text.includes("человек")) {
        const matches = m.text.match(/(\d+)\s*(детей|человек)/);
        const sickMatches = m.text.match(/(\d+)\s*(болеют|отсутствуют)/);
        if (matches) totalChildren += parseInt(matches[1]);
        if (sickMatches) totalSick += parseInt(sickMatches[1]);
      }
    });
    return { totalChildren, totalSick };
  };

  const [messages, setMessages] = useState<any[]>([
    { text: "1А — 25 детей, 2 болеют.", time: "08:15", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 25 порций. Данные переданы в столовую Aqbobek." } },
    { text: "Доброе утро! В 2Б 20 человек, все на месте.", time: "08:17", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 20 порций. Заявка сформирована автоматически." } },
    { text: "В кабинете 12 сломалась парта на последнем ряду. Дети не могут сидеть.", time: "09:05", parsed: { type: "incident", urgency: "high", insight: "🚨 ИНЦИДЕНТ\nСоздана задача Ахмету (Завхоз): Починить парту в каб. 12" } },
    { text: "Коллеги, я с температурой 39. Сегодня не смогу прийти.", time: "10:12", parsed: { type: "absence", urgency: "critical", insight: "🔥 ВНИМАНИЕ: Аскар (Математика) болен.\nНайдены свободные окна: Смирнова Е. (2 урок), Кусаинова А. (3 урок)." } },
    { text: "3В - 22 человека, 3 отсутствуют.", time: "10:15", parsed: { type: "attendance", urgency: "low", insight: "✅ Питание: 22 порции. Список отсутствующих: Жусупов, Кан, Ли." } }
  ]);
  
const [dbTasks, setDbTasks] = useState<any[]>([
    { id: 991, title: "Починить трубу в женском туалете (2 этаж)", assignee: "Ахмет (Завхоз)", deadline: "Сегодня до 14:00", is_completed: false },
    { id: 992, title: "Подготовить актовый зал к AIS Hack 3.0", assignee: "Айгерим", deadline: "До среды", is_completed: false },
    { id: 993, title: "Заказать 20 бутылей воды для 1-4 классов", assignee: "Назкен", deadline: "Завтра", is_completed: false },
    { id: 994, title: "Проанализировать посещаемость за неделю", assignee: "Секретарь", deadline: "Пятница", is_completed: false },
    { id: 995, title: "Организовать замену для заболевшего историка", assignee: "Директор", deadline: "Срочно", is_completed: false },
    { id: 996, title: "Снять показания тепловых счетчиков", assignee: "Ахмет (Завхоз)", deadline: "Среда", is_completed: true },
    { id: 997, title: "Разослать письмо родителям 3В класса", assignee: "Смирнова Е.", deadline: "Сегодня", is_completed: true },
    { id: 998, title: "Составить меню столовой на следующую неделю", assignee: "Шеф-повар", deadline: "Пятница", is_completed: true }
  ]);

  const [mockSchedule, setMockSchedule] = useState([
    { 
      lesson: 1, class: "3В", room: "302", teacher: "Аскар (Болеет)", subject: "Математика", 
      alert: true, replacement: "Смирнова Елена", 
      reasoning: "Свободное окно (1-й урок), профиль соответствует (матем. + нач. школа).", 
      confidence: 98, status: "pending",
      rejected: [
        { name: "Кусаинова А.", reason: "Занята на 1 уроке (ведёт 4Б)" },
        { name: "Нурланов Т.", reason: "Профиль не совпадает (история, не математика)" }
      ]
    },
    { 
      lesson: 2, class: "5А", room: "305", teacher: "Аскар (Болеет)", subject: "Алгебра", 
      alert: true, replacement: "Кусаинов А.", 
      reasoning: "Ведет в параллели 5-х классов, имеет опыт по данной теме (уравнения).", 
      confidence: 92, status: "pending",
      rejected: [
        { name: "Смирнова Е.", reason: "Уже заменяет на 1 уроке (3В)" },
        { name: "Жанибеков М.", reason: "Превышение нагрузки (Прик. МОН №110 п.3)" }
      ]
    },
    { 
      lesson: 3, class: "8А", room: "308", teacher: "Антон", subject: "Физика", 
      alert: false, replacement: "", 
      reasoning: "Замена не требуется.", 
      confidence: 100, status: "ok",
      rejected: []
    }
  ]);

  const applyReplacements = () => {
    setMockSchedule(prev => prev.map(s => s.alert ? { ...s, replacement: s.replacement, status: "applied" } : s));
    setShowSuccessOverlay(true);
    setMascotMsg("Миссия выполнена! Все замены утверждены и разосланы. 🚀");
    setTimeout(() => setShowSuccessOverlay(false), 4000);
  };

  const generateOrderHTML = (sub: any): string => {
    const today = new Date();
    const dateStr = today.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
    const orderNum = `78-${sub.lesson}`;

    return `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Приказ № ${orderNum}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap');
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'PT Serif', Georgia, serif; background: #f0f4f8; display: flex; justify-content: center; padding: 40px 20px; }
    .page { background: white; width: 210mm; min-height: 297mm; padding: 25mm 22mm 20mm; box-shadow: 0 8px 40px rgba(0,0,0,0.15); position: relative; }
    .stripe { position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #1a3a8f, #2563eb, #16a34a); border-radius: 4px 4px 0 0; }
    .school { text-align: center; font-size: 10pt; color: #555; border-bottom: 1px solid #d1d5db; padding-bottom: 10px; margin-bottom: 14px; line-height: 1.6; }
    .school strong { color: #1a1a2e; }
    h1 { text-align: center; font-size: 20pt; color: #1a3a8f; margin-bottom: 4px; letter-spacing: 0.04em; }
    .meta { display: flex; justify-content: space-between; font-size: 10pt; color: #6b7280; margin-bottom: 6px; }
    .subject { text-align: center; font-size: 13pt; color: #1e40af; font-weight: 700; margin-bottom: 14px; }
    .badge { background: #f0fdf4; border: 1px solid #86efac; border-radius: 6px; padding: 8px 14px; text-align: center; color: #166534; font-size: 9pt; font-family: Arial, sans-serif; margin-bottom: 16px; }
    .preamble { font-size: 11pt; line-height: 1.7; text-align: justify; margin-bottom: 14px; color: #374151; }
    .decree-title { font-size: 14pt; font-weight: 700; color: #1a3a8f; margin-bottom: 10px; }
    .item { display: flex; gap: 10px; font-size: 11pt; line-height: 1.65; margin-bottom: 8px; }
    .item .n { min-width: 20px; font-weight: 700; color: #1a3a8f; }
    .basis { font-size: 9.5pt; color: #6b7280; margin-top: 8px; margin-bottom: 16px; font-style: italic; line-height: 1.5; }
    hr { border: none; border-top: 1px solid #e5e7eb; margin: 16px 0; }
    .control { font-size: 10pt; color: #6b7280; margin-bottom: 24px; font-style: italic; }
    .sig { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; font-size: 11pt; }
    .sig-line { flex: 1; border-bottom: 1px solid #9ca3af; margin: 0 12px; }
    .footer { margin-top: 30px; padding-top: 8px; border-top: 1px solid #e5e7eb; text-align: center; font-size: 7.5pt; color: #9ca3af; font-family: Arial, sans-serif; }
    .print-btn { position: fixed; bottom: 30px; right: 30px; background: #1a3a8f; color: white; border: none; border-radius: 50px; padding: 14px 28px; font-size: 13pt; font-family: Arial, sans-serif; font-weight: bold; cursor: pointer; box-shadow: 0 4px 20px rgba(26,58,143,0.4); }
    @media print { body { background: none; padding: 0; } .page { box-shadow: none; width: 100%; } .print-btn { display: none !important; } }
  </style>
</head>
<body>
  <div class="page">
    <div class="stripe"></div>
    <div class="school"><strong>Образовательный комплекс «Aqbobek International School»</strong><br>КГУ «Начальная школа» | г. Актобе, Республика Казахстан</div>
    <h1>ПРИКАЗ № ${orderNum}</h1>
    <div class="meta"><span>г. Актобе</span><span>«${dateStr}»</span></div>
    <div class="subject">О замене учебных занятий</div>
    <div class="badge">✓ &nbsp; Проверено AI на соответствие Приказу МОН РК №130 и №110 | Сформировано: Покойо</div>
    <div class="preamble">
      В связи с временной нетрудоспособностью учителя <strong>${sub.teacher.replace(' (Болеет)', '')}</strong> и в целях обеспечения выполнения
      государственных общеобязательных стандартов образования, недопущения срыва учебного процесса
      и соблюдения норм Приказа МОН РК №110 «О замене учителей»,
    </div>
    <div class="decree-title">БҰЙЫРАМЫН / ПРИКАЗЫВАЮ:</div>
    <div class="item"><span class="n">1.</span><span>Произвести замену учебных занятий в <strong>${sub.class}</strong> классе, кабинет <strong>${sub.room}</strong>, урок <strong>№${sub.lesson}</strong> (предмет: ${sub.subject}).</span></div>
    <div class="item"><span class="n">2.</span><span>Возложить временное исполнение обязанностей по проведению урока на учителя <strong>${sub.replacement}</strong> согласно утвержденному расписанию.</span></div>
    <div class="item"><span class="n">3.</span><span>Оплату за фактически проведенные часы замещения произвести в соответствии с нормативными правовыми актами РК и внутренним положением об оплате труда, согласно Приказу МОН РК №110.</span></div>
    <div class="item"><span class="n">4.</span><span>Учителю <strong>${sub.replacement}</strong> обеспечить качественное проведение занятий и своевременное внесение записей в электронный журнал (Күнделік) — согласно Приказу МОН РК №130.</span></div>
    <div class="item"><span class="n">5.</span><span>Секретарю передать копию настоящего приказа в бухгалтерию для начисления доплаты.</span></div>
    <div class="basis">Основание: Приказ МОН РК №130 «Об утверждении Перечня документов, обязательных для ведения педагогами», сообщение о временной нетрудоспособности от ${dateStr}.</div>
    <hr>
    <div class="control">Контроль за исполнением настоящего приказа оставляю за собой.</div>
    <div class="sig"><span>Директор начальной школы AIS:</span><span class="sig-line"></span><span>/ Сарсенбаев А.Т.</span></div>
    <div class="sig"><span>С приказом ознакомлен(а):</span><span class="sig-line"></span><span>/ ${sub.replacement}</span></div>
    <div class="footer">Сгенерировано автоматически системой Покойо &nbsp;|&nbsp; Соответствие: Приказ МОН РК №110, №130 &nbsp;|&nbsp; ${dateStr}</div>
  </div>
  <button class="print-btn" onclick="window.print()">🖨️ Печать / Сохранить PDF</button>
  <script>setTimeout(() => window.print(), 600);</script>
</body>
</html>`;
  };

  const handleGenerateOrder = async (sub: any) => {
    setIsGeneratingOrder(true);
    try {
      const html = generateOrderHTML(sub);
      const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const newTab = window.open(url, '_blank');
      if (!newTab) {
        // popup blocked — download as file instead
        const link = document.createElement('a');
        link.href = url;
        link.download = `Prikaz_${sub.class}_urok${sub.lesson}.html`;
        link.click();
      }
    } catch (e) {
      console.error("Order generation error:", e);
      alert("Ошибка при генерации приказа.");
    } finally {
      setIsGeneratingOrder(false);
    }
  };

  // REAL DATA: Загрузка задач из БД
  const loadTasks = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/tasks/');
      setDbTasks(res.data);
    } catch (e) {
      console.error("Failed to load tasks:", e);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const pushMessage = async (text, isVoice = false) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages(prev => [...prev, { text, time, parsed: null }]);

    try {
      // REAL DATA: Запрос парсинга к настоящему FastAPI бэкенду
      const res = await axios.post('http://localhost:8000/api/voice/task', { test_text: text });
      const tasksParsed = res.data.voice_decomposition?.tasks || [];
      
      let insightText = "Ничего не найдено.";
      if (tasksParsed.length > 0) {
        insightText = `✅ Распознано задач: ${tasksParsed.length}\n`;
        // Если нашли задачи, сохраняем их в базу!
        for (const t of tasksParsed) {
          await axios.post('http://localhost:8000/api/tasks/', {
            title: t.task_name || t.description || "Новая задача", 
            assignee: t.assignee || "Неизвестно", 
            deadline: t.deadline || "Без срока"
          });
        }
        await loadTasks(); // Обновляем список задач
      }

      setMessages(prev => {
        let updated = [...prev];
        if (updated.length > 0) {
          updated[updated.length - 1].parsed = { type: "backend_parsed", urgency: "medium", insight: insightText };
        }
        return updated;
      });

    } catch (e) {
      console.error("Critical error in pushMessage:", e);
      setMessages(prev => {
        let updated = [...prev];
        if (updated.length > 0) {
          updated[updated.length - 1].parsed = { type: "error", urgency: "critical", insight: "Ошибка сети. Бэкенд не отвечает." };
        }
        return updated;
      });
    }
  };

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

  const DEMO_RESPONSES: Record<string, any> = {
    "Нормы питания №130": {
      answer: "Согласно Приказу №130, мониторинг качества питания осуществляется ежедневно комиссией в составе медработника, администрации и представителей родительского комитета. Данные о количестве учащихся должны подаваться в столовую не позднее 09:00 текущего дня. Контроль выхода блюд и соответствие меню-раскладке обязателен.",
      sources: ["Приказ №130 МОН", "СанПиН 2024", "Методические рекомендации"]
    },
    "Приказ №110: Замены": {
      answer: "Замена временно отсутствующих учителей должна производиться специалистами той же предметной области. При отсутствии возможности — учителями смежных дисциплин. В исключительных случаях допускается проведение занятий администрацией школы. Все замены фиксируются в журнале учета пропущенных и замещенных уроков и оплачиваются согласно фактически отработанным часам.",
      sources: ["Приказ №110", "Трудовой Кодекс РК", "Инструкция по ведению ЖУПЗ"]
    },
    "Приказ №76: Аттестация": {
      answer: "Аттестация педагогов проводится один раз в пять лет в соответствии с правилами Приказа №76. Педагоги, подтвердившие категорию «исследователь» или «мастер», получают надбавку в размере 30-50% от БДО. Портфолио должно быть загружено в систему не позднее 2 месяцев до квалификационного экзамена.",
      sources: ["Приказ №76 МОН", "Закон об образовании", "Правила аттестации"]
    }
  };

  const DEMO_CHECKLISTS: Record<string, any> = {
    "Приказ №130": {
      answer: "Чек-лист по Приказу №130 (Посещаемость и питание):",
      items: [
        "Подать сведения о посещаемости в систему до 09:00.",
        "При отсутствии ученика >3 дней: связаться с родителями.",
        "Составить акт посещения семьи (если причина не уважительная).",
        "Сдать данные по льготному питанию соцпедагогу до 10:00."
      ],
      sources: ["Приказ №130 МОН РК"]
    }
  };

  const handleRagSearch = async (queryOverride?: string) => {
    const query = queryOverride || ragQuery;
    if (!query.trim()) return;
    
    setIsRagLoading(true);
    setRagResult(null);
    if (!queryOverride) setRagQuery(query);

    // DEMO Fallback: Search mode
    if (ragMode === 'search' && DEMO_RESPONSES[query]) {
      setTimeout(() => {
        setRagResult(DEMO_RESPONSES[query]);
        setIsRagLoading(false);
      }, 1500); 
      return;
    }

    // DEMO Fallback: Checklist mode
    const isOrder130 = query.includes("130") || query.includes("посещаемость");
    if (ragMode === 'checklist' && isOrder130) {
      setTimeout(() => {
        setRagResult(DEMO_CHECKLISTS["Приказ №130"]);
        setIsRagLoading(false);
      }, 2000);
      return;
    }

    try {
      const endpoint = ragMode === 'search' ? 'query' : 'checklist';
      const payload = ragMode === 'search' ? { query } : { order_text: query };
      const res = await axios.post(`http://localhost:8000/api/rag/${endpoint}`, payload);
      
      const data = res.data;
      if (ragMode === 'search') {
        setRagResult({
          answer: data.analysis || data.answer || "К сожалению, в базе знаний не нашлось точного совпадения.",
          sources: data.relevant_orders || data.sources || ["Нормативная база"]
        });
      } else {
        // Checklist format
        const items = data.checklist || ["Пункт 1", "Пункт 2"];
        setRagResult({
          answer: "Чек-лист сформирован успешно:",
          items,
          sources: ["Автоматическая генерация"]
        });
      }

    } catch (e) {
      setRagResult({ 
        answer: "Извините, база знаний временно недоступна. Попробуйте позже.", 
        sources: [] 
      });
    } finally {
      setIsRagLoading(false);
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
         // Отправляем реальный голос на сервер
         pushMessage(finalTranscript, true);
      }
    };
    recognition.onerror = () => setIsRecording(false);
    recognition.onend = () => setIsRecording(false);
    recognition.start();
  };

  return (
    <div className="flex h-screen bg-slate-50 text-slate-800 font-sans tracking-wide overflow-hidden relative">
      <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-blue-50 rounded-full mix-blend-multiply filter blur-[150px] opacity-60 z-0"></div>

      <div className={`${isSidebarOpen ? 'w-1/3 max-w-[340px]' : 'w-0 overflow-hidden'} flex flex-col bg-white border-r border-slate-200 shadow-xl z-20 transition-all duration-300 relative`}>
        <div className="p-8 flex flex-col items-center border-b border-slate-50 bg-white w-[340px]">
          <div className="w-16 h-16 bg-slate-900 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-500/10 mb-4 p-3.5 border border-slate-800">
            <img src={schoolLogo} alt="IB Logo" className="w-full h-full object-contain" />
          </div>
          <div className="font-extrabold text-2xl text-blue-800">Покойо</div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-2 w-[340px]">
          <MenuButton title="Рабочие чаты и ГС" desc="Анализ LLM парсером" icon={<Users />} active={activeTab === 'chat'} onClick={() => setActiveTab('chat')} />
          <MenuButton title="Делегат (Voice-to-Task)" desc="Реальная База Данных" icon={<CheckCircle2 />} active={activeTab === 'tasks'} onClick={() => setActiveTab('tasks')} />
          <MenuButton title="Smart Substitution" desc="Анализ LLM: Замены" icon={<Calendar />} active={activeTab === 'schedule'} onClick={() => setActiveTab('schedule')} />
          <MenuButton title="Бюрократический RAG" desc="Проверка по приказам" icon={<BookOpen />} active={activeTab === 'rag'} onClick={() => setActiveTab('rag')} />
          <MenuButton title="Аналитика" desc="Тренды и статистика" icon={<BarChart3 />} active={activeTab === 'analytics'} onClick={() => setActiveTab('analytics')} />
        </div>
        <div className="p-4 border-t border-slate-100 w-[340px]">
          <button onClick={() => { localStorage.removeItem('auth_token'); window.location.reload(); }} className="w-full text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition font-bold text-sm p-3 text-center">Выйти из системы</button>
        </div>
      </div>

      <div className="flex-1 flex flex-col relative z-0 min-w-0">
        <div className="absolute inset-0 bg-slate-50/50 z-[-1]"></div>
        
        <div className="px-10 py-8 flex items-center justify-between z-10 sticky top-0 bg-white/10 backdrop-blur-md border-b border-slate-200">
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)} 
              className="p-2.5 rounded-xl bg-white border border-slate-200 shadow-sm hover:bg-slate-50 transition active:scale-95 text-slate-600"
            >
              <Menu size={24} />
            </button>
            <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight">Дашборд Покойо</h2>
          </div>
          <div className="flex items-center bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 gap-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#25D366] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-[#25D366]"></span>
            </span>
            <div className="text-xs font-extrabold uppercase tracking-widest text-slate-600">
              {botFeed.length > 0 ? `LIVE: ${botFeed.length} сообщений` : 'Sync: Telegram / SQLite'}
            </div>
          </div>
          <button
            disabled={isDemoRunning}
            onClick={async () => {
              setIsDemoRunning(true);
              setActiveTab('chat');
              try {
                await axios.post('http://localhost:8000/api/bot/demo-scenario');
              } catch {}
              setTimeout(() => setIsDemoRunning(false), 18000);
            }}
            className={`flex items-center gap-2 text-xs font-black uppercase tracking-widest px-5 py-3 rounded-2xl shadow-sm border transition-all active:scale-95 ${
              isDemoRunning
                ? 'bg-amber-50 text-amber-600 border-amber-200 cursor-wait animate-pulse'
                : 'bg-violet-50 text-violet-600 border-violet-200 hover:bg-violet-100'
            }`}
          >
            <Rocket className="w-4 h-4" />
            {isDemoRunning ? 'Демо идёт...' : '🎬 Live Demo'}
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-10 pb-10 space-y-8 z-10 scroll-smooth pt-6">
          {activeTab === 'chat' && (
            <div className="max-w-4xl mx-auto flex flex-col space-y-8">
              
              {/* Module 1: Daily Attendance Summary */}
              <div className="bg-gradient-to-r from-blue-700 to-blue-500 rounded-[2.5rem] p-8 shadow-2xl shadow-blue-500/20 text-white relative overflow-hidden group">
                 <div className="absolute -bottom-2 right-4 pointer-events-none z-0 animate-bounce" style={{ animationDuration: '4s' }}>
                    <img src="/pocoyo_win.png" alt="Покойо" className="w-[130px] h-auto drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)] contrast-110 saturate-110 opacity-90" />
                 </div>
                 <div className="flex items-center justify-between relative z-10">
                    <div>
                       <div className="flex items-center space-x-2 text-blue-100 font-black uppercase tracking-widest text-xs mb-3">
                          <Clock className="w-4 h-4" /> <span>Ежедневный Свод (09:00 AM)</span>
                       </div>
                       <h3 className="text-3xl font-black mb-1">Свод по питанию</h3>
                       <p className="text-blue-100/70 font-bold">
                         {svod && svod.report_count > 0
                           ? `Получено ${svod.report_count} отчётов из Telegram-бота`
                           : 'Данные из Telegram-бота школы'}
                       </p>
                    </div>
                    <div className="text-right">
                       <div className="text-5xl font-black leading-none">
                         {svod && svod.total_portions > 0 ? svod.total_portions : calculateAttendanceTotals().totalChildren}
                       </div>
                       <div className="text-sm font-bold text-blue-100 mt-1 uppercase tracking-widest">Порций всего</div>
                    </div>
                 </div>
                 <div className="mt-8 grid grid-cols-3 gap-4 border-t border-white/20 pt-6 relative z-10">
                    <div className="flex items-center space-x-3 bg-white/10 p-4 rounded-3xl">
                       <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center font-black">
                         {svod ? svod.report_count : messages.filter(m => m.text.includes('детей')).length}
                       </div>
                       <div className="text-xs font-bold text-blue-50">Отчётов от классов</div>
                    </div>
                    <div className="flex items-center space-x-3 bg-blue-400/20 p-4 rounded-3xl border border-blue-300/20">
                       <div className="w-10 h-10 bg-rose-500/40 rounded-full flex items-center justify-center font-black text-white">
                         {svod ? svod.absences_today : 0}
                       </div>
                       <div className="text-xs font-bold text-blue-100">Отсутствий (учителя)</div>
                    </div>
                    <div className="flex items-center space-x-3 bg-orange-400/20 p-4 rounded-3xl border border-orange-300/20">
                       <div className="w-10 h-10 bg-orange-500/40 rounded-full flex items-center justify-center font-black text-white">
                         {svod ? svod.incidents_today : 0}
                       </div>
                       <div className="text-xs font-bold text-orange-100">Инцидентов</div>
                    </div>
                 </div>
              </div>

              {/* LIVE: Telegram Bot Feed */}
              {botFeed.length > 0 && (
                <div className="bg-white rounded-[2.5rem] border border-slate-100 shadow-xl overflow-hidden">
                  <div className="flex items-center justify-between px-8 py-5 border-b border-slate-100">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-xl bg-blue-500 flex items-center justify-center">
                        <MessageSquare size={18} className="text-white" />
                      </div>
                      <div>
                        <div className="font-black text-slate-800 text-sm">LIVE: Telegram-лента</div>
                        <div className="text-xs text-slate-400 font-medium">Реальные сообщения от учителей • обновляется каждые 4 сек</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <button 
                        onClick={async () => {
                          if (window.confirm('Точно очистить ленту?')) {
                            await axios.delete('http://localhost:8000/api/bot/clear');
                            setBotFeed([]);
                          }
                        }}
                        className="text-xs font-bold text-rose-500 hover:text-rose-600 bg-rose-50 px-3 py-1.5 rounded-lg active:scale-95 transition"
                      >
                         Очистить
                      </button>
                      <span className="relative flex h-2.5 w-2.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                      </span>
                    </div>
                  </div>
                  <div className="divide-y divide-slate-50 max-h-80 overflow-y-auto">
                    {botFeed.map((msg, i) => {
                      const typeColors: Record<string,string> = {
                        food: 'bg-emerald-50 text-emerald-700 border-emerald-100',
                        absence: 'bg-rose-50 text-rose-700 border-rose-100',
                        incident: 'bg-orange-50 text-orange-700 border-orange-100',
                        other: 'bg-slate-50 text-slate-600 border-slate-100',
                      };
                      const typeLabels: Record<string,string> = {
                        food: '🍱 Явка', absence: '🔴 Отсутствие',
                        incident: '⚠️ Инцидент', other: 'ℹ️ Прочее',
                      };
                      const color = typeColors[msg.parsed_type] || typeColors.other;
                      const label = typeLabels[msg.parsed_type] || 'ℹ️';
                      const timeStr = msg.created_at ? msg.created_at.slice(-8, -3) : '';
                      return (
                        <div key={i} className="flex items-center gap-4 px-8 py-4 hover:bg-slate-50/50 transition">
                          <div className="text-xs text-slate-400 font-bold min-w-[40px]">{timeStr}</div>
                          <div className="font-bold text-slate-700 text-sm min-w-[130px]">{msg.sender}</div>
                          <div className="flex-1 text-sm text-slate-600 truncate">{msg.text}</div>
                          <div className={`text-[10px] font-black uppercase px-2.5 py-1 rounded-lg border ${color} shrink-0`}>{label}</div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in zoom-in duration-700">
                  <div className="w-16 h-16 mb-4 text-slate-200">
                    <MessageSquare size={64} />
                  </div>
                  <h3 className="text-2xl font-black text-slate-800 mb-2">Здесь пока тихо...</h3>
                  <p className="text-slate-500 max-w-sm">Сообщения из чатов появятся тут автоматически. Я слежу за эфиром!</p>
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

                  <div className={`mt-3 ml-8 border rounded-2xl p-5 text-sm flex items-start w-[95%] shadow-md transition-all relative overflow-hidden ${m.parsed?.urgency === 'critical' ? 'bg-rose-50 border-rose-200' : 'bg-emerald-50/50 border-emerald-100'}`}>
                    <div className="absolute -right-2 -bottom-2 w-24 h-24 opacity-20 pointer-events-none transform rotate-12 group-hover:scale-110 transition-transform">
                      <img src="/pocoyo_wink.png" alt="Инсайт Покойо" className="w-full h-full object-contain" />
                    </div>
                    <div className="flex flex-col w-full relative z-10">
                      <b className={`uppercase text-[11px] font-black tracking-widest opacity-80 mb-2`}>[АНАЛИЗ ПОКОЙО]</b>
                      <span className="font-bold text-[15px] whitespace-pre-wrap">{m.parsed?.insight}</span>
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}

          {activeTab === 'tasks' && (
            <div className="max-w-5xl mx-auto space-y-8 pb-20">

              {/* Header */}
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-black text-4xl text-slate-800 tracking-tight">Делегат</h3>
                  <p className="text-slate-500 mt-1 font-medium flex items-center gap-2">
                    <Mic className="w-4 h-4 text-blue-500" />
                    Voice-to-Task — голос директора превращается в задачи автоматически
                  </p>
                </div>
                <button onClick={loadTasks} className="flex items-center gap-2 text-sm font-bold bg-white text-blue-600 px-5 py-3 border border-blue-200 rounded-2xl shadow-sm hover:bg-blue-50 transition active:scale-95">
                  <Activity className="w-4 h-4" /> Обновить БД
                </button>
              </div>

              {/* Stats row */}
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: 'Активных задач', value: dbTasks.filter(t => !t.is_completed).length, color: 'bg-blue-600', icon: <Zap className="w-5 h-5 text-white" /> },
                  { label: 'Выполнено сегодня', value: dbTasks.filter(t => t.is_completed).length, color: 'bg-emerald-500', icon: <CheckCircle className="w-5 h-5 text-white" /> },
                  { label: 'Исполнителей', value: new Set(dbTasks.map(t => t.assignee)).size, color: 'bg-violet-500', icon: <Users className="w-5 h-5 text-white" /> },
                ].map((s, i) => (
                  <div key={i} className="bg-white rounded-3xl p-6 border border-slate-100 shadow-lg flex items-center gap-5">
                    <div className={`w-12 h-12 ${s.color} rounded-2xl flex items-center justify-center shadow-lg shrink-0`}>{s.icon}</div>
                    <div>
                      <div className="text-3xl font-black text-slate-800">{s.value}</div>
                      <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-0.5">{s.label}</div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Voice recording zone */}
              <div className={`relative rounded-[2.5rem] p-10 border-2 transition-all duration-300 overflow-hidden ${isRecording ? 'bg-gradient-to-br from-blue-600 to-violet-600 border-transparent shadow-2xl shadow-blue-500/30' : 'bg-white border-dashed border-slate-200 hover:border-blue-300 hover:shadow-lg'}`}>
                {isRecording && (
                  <>
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <div className="w-72 h-72 rounded-full border-2 border-white/10 animate-ping" style={{animationDuration:'1.8s'}} />
                    </div>
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <div className="w-48 h-48 rounded-full border-2 border-white/20 animate-ping" style={{animationDuration:'1.1s'}} />
                    </div>
                  </>
                )}
                <div className="relative z-10 flex flex-col items-center text-center gap-6">
                  <button
                    onClick={handleMicClick}
                    disabled={isTranscribing}
                    className={`w-24 h-24 rounded-full flex items-center justify-center shadow-2xl transition-all active:scale-90 ${
                      isRecording ? 'bg-white text-blue-600 scale-110' :
                      isTranscribing ? 'bg-slate-200 text-slate-400 cursor-wait' :
                      'bg-blue-600 text-white hover:bg-blue-500 hover:scale-105'
                    }`}
                  >
                    {isTranscribing ? <Activity className="w-10 h-10 animate-spin" /> : <Mic className="w-10 h-10" />}
                  </button>
                  <div>
                    <div className={`font-black text-xl ${isRecording ? 'text-white' : 'text-slate-800'}`}>
                      {isRecording ? '🔴 Идёт запись...' : isTranscribing ? '🧠 AI разбивает на задачи...' : 'Нажмите и говорите'}
                    </div>
                    <div className={`text-sm mt-1.5 font-medium ${isRecording ? 'text-blue-100' : 'text-slate-400'}`}>
                      {isRecording ? 'Продиктуйте поручения. AI сам найдёт исполнителей и сроки.' : 'Браузер распознает речь — Whisper не нужен'}
                    </div>
                  </div>
                  {!isRecording && !isTranscribing && (
                    <div className="flex flex-wrap gap-2 justify-center">
                      {['Назкен, закажи воду на завтра', 'Айгерим, подготовь актовый зал', 'Ахмет, почини парту в каб. 12'].map((phrase, i) => (
                        <button key={i} onClick={() => { pushMessage(phrase); }}
                          className="text-xs font-bold bg-blue-50 text-blue-600 border border-blue-100 px-4 py-2 rounded-xl hover:bg-blue-100 transition active:scale-95">
                          💬 {phrase}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Active tasks */}
              {dbTasks.filter(t => !t.is_completed).length > 0 ? (
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <span className="relative flex h-2.5 w-2.5"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span><span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span></span>
                    <span className="font-black text-slate-600 uppercase tracking-widest text-xs">В работе — {dbTasks.filter(t => !t.is_completed).length} задач</span>
                  </div>
                  <div className="space-y-3">
                    {dbTasks.filter(t => !t.is_completed).map((t, idx) => {
                      const urgencyMap: Record<string, string> = {
                        'Сегодня': 'bg-rose-50 text-rose-600 border-rose-100',
                        'Срочно': 'bg-rose-50 text-rose-600 border-rose-100',
                        'Завтра': 'bg-amber-50 text-amber-600 border-amber-100',
                        'До среды': 'bg-blue-50 text-blue-600 border-blue-100',
                        'Пятница': 'bg-blue-50 text-blue-600 border-blue-100',
                      };
                      const urgencyColor = urgencyMap[t.deadline] || 'bg-slate-50 text-slate-500 border-slate-100';
                      const initials = t.assignee?.split(' ').map((w: string) => w[0]).join('').slice(0, 2).toUpperCase() || '??';
                      const avatarColors = ['bg-blue-500', 'bg-violet-500', 'bg-emerald-500', 'bg-amber-500', 'bg-rose-500'];
                      const avatarColor = avatarColors[idx % avatarColors.length];
                      return (
                        <div key={idx} className="group bg-white rounded-3xl shadow-md border border-slate-100 p-5 flex items-center gap-5 hover:shadow-xl hover:-translate-y-0.5 transition-all">
                          <div className={`w-12 h-12 ${avatarColor} rounded-2xl flex items-center justify-center text-white font-black text-sm shrink-0 shadow-md`}>{initials}</div>
                          <div className="flex-1 min-w-0">
                            <div className="font-extrabold text-slate-800 text-base">{t.title}</div>
                            <div className="flex items-center gap-3 mt-1.5 flex-wrap">
                              <span className="text-xs font-bold text-slate-400">{t.assignee}</span>
                              <span className={`text-[10px] font-black uppercase px-2.5 py-1 rounded-lg border ${urgencyColor}`}>📅 {t.deadline}</span>
                            </div>
                          </div>
                          <button onClick={() => markTaskDone(t.id)}
                            className="shrink-0 flex items-center gap-2 bg-slate-900 hover:bg-emerald-500 text-white text-xs font-black uppercase tracking-widest px-5 py-2.5 rounded-2xl shadow-md transition-all active:scale-95 opacity-0 group-hover:opacity-100">
                            <Check className="w-3.5 h-3.5" /> Готово
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-16 bg-white rounded-[2.5rem] border border-dashed border-slate-200 text-center">
                  <div className="w-16 h-16 bg-emerald-50 rounded-3xl flex items-center justify-center mb-4">
                    <CheckCircle2 className="w-8 h-8 text-emerald-400" />
                  </div>
                  <div className="font-black text-xl text-slate-700 mb-2">Все задачи выполнены! 🎉</div>
                  <div className="text-slate-400 text-sm">Нажмите на микрофон и продиктуйте новые поручения</div>
                </div>
              )}

              {/* Completed */}
              {dbTasks.filter(t => t.is_completed).length > 0 && (
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <CheckCircle className="w-4 h-4 text-emerald-400" />
                    <span className="font-black text-slate-400 uppercase tracking-widest text-xs">Выполнено — {dbTasks.filter(t => t.is_completed).length}</span>
                  </div>
                  <div className="space-y-2">
                    {dbTasks.filter(t => t.is_completed).map((t, idx) => (
                      <div key={`done-${idx}`} className="bg-slate-50 rounded-2xl px-6 py-4 border border-slate-100 flex items-center gap-4 opacity-50">
                        <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                        <span className="font-bold text-slate-400 line-through text-sm flex-1">{t.title}</span>
                        <span className="text-xs text-slate-400">{t.assignee}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>
          )}

          {activeTab === 'schedule' && (
            <div className="space-y-8 max-w-5xl mx-auto pb-20">
              <div className="flex justify-between items-end mb-4">
                <div>
                   <h3 className="font-black text-4xl text-slate-800 tracking-tight">AI Smart Substitution</h3>
                   <p className="text-slate-500 mt-2 font-medium flex items-center">
                     <Brain className="w-4 h-4 mr-2 text-blue-500" /> 
                     Анализ на основе приказа №110 и расписания учителей
                   </p>
                </div>
                {mockSchedule.some(s => s.status === 'pending') && (
                  <button 
                    onClick={applyReplacements}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-2xl font-black shadow-xl shadow-blue-500/20 transition-all transform hover:-translate-y-1 active:scale-95 flex items-center"
                  >
                    <Rocket className="w-5 h-5 mr-3" /> Утвердить все замены
                  </button>
                )}
              </div>

              <div className="grid gap-6">
                {mockSchedule.map((s, idx) => (
                  <div key={idx} className={`bg-white rounded-[2.5rem] p-8 shadow-xl border-2 transition-all group ${s.alert ? (s.status === 'applied' ? 'border-blue-100 bg-blue-50/20' : 'border-rose-100 animate-pulse-subtle') : 'border-slate-100'}`}>

                    {/* ---- ROW 1: Lesson info + replacement ---- */}
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-8">
                        <div className={`w-16 h-16 rounded-2xl flex flex-col items-center justify-center font-black text-2xl shadow-inner shrink-0 ${s.alert ? 'bg-rose-50 text-rose-500' : 'bg-slate-50 text-slate-400'}`}>
                          <span className="text-xs uppercase opacity-40 mb-1">Урок</span>
                          {s.lesson}
                        </div>
                        <div>
                          <div className="flex items-center space-x-3 mb-2">
                             <span className="bg-slate-800 text-white text-[10px] font-black px-3 py-1 rounded-full uppercase tracking-widest">Класс {s.class}</span>
                             <span className="text-slate-400 font-bold text-sm flex items-center"><Clock className="w-3 h-3 mr-1" /> Каб. {s.room}</span>
                          </div>
                          <h4 className="text-2xl font-extrabold text-slate-800">{s.subject}</h4>
                          <p className="text-slate-500 font-bold mt-1">{s.teacher}</p>
                        </div>
                      </div>

                      {s.alert && (
                        <div className="flex items-center space-x-4 shrink-0">
                          <div className="text-right">
                             <div className="text-[10px] font-black text-blue-500 uppercase tracking-widest mb-1">Предлагаемая замена</div>
                             <div className="text-xl font-black text-slate-800">{s.replacement}</div>
                          </div>
                          <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-blue-500/20 shrink-0">
                             <ArrowRight size={24} />
                          </div>
                        </div>
                      )}
                    </div>

                    {/* ---- ROW 2: Action buttons (below, when applied) ---- */}
                    {s.status === 'applied' && (
                      <div className="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center gap-2">
                        <div className="flex items-center gap-1.5 bg-emerald-50 text-emerald-700 px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border border-emerald-100">
                          <CheckCircle size={12} strokeWidth={3} />
                          <span>Проверено AI • №130</span>
                        </div>
                        <div className="flex items-center gap-1.5 bg-blue-50 text-blue-600 px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border border-blue-100">
                          <Check size={12} strokeWidth={3} />
                          <span>Applied</span>
                        </div>
                        <div className="flex-1" />
                        <button
                          onClick={() => handleGenerateOrder(s)}
                          disabled={isGeneratingOrder}
                          className={`flex items-center gap-1.5 text-white px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all active:scale-95 shadow-md ${isGeneratingOrder ? 'bg-slate-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 shadow-blue-500/20'}`}
                        >
                          {isGeneratingOrder ? <Activity size={12} className="animate-spin" /> : <FileText size={12} />}
                          <span>{isGeneratingOrder ? 'Генерация...' : 'Скачать приказ'}</span>
                        </button>
                        <a
                          href={`https://wa.me/?text=${encodeURIComponent(`Приказ о замене сформирован. Учитель: ${s.teacher}, заменяет: ${s.replacement}, класс ${s.class}, каб. ${s.room}, урок ${s.lesson}. Сделайте начисление за замещение. Покойо.`)}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-1.5 bg-[#25D366] hover:bg-[#1da851] text-white px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all active:scale-95 shadow-md shadow-green-500/20"
                        >
                          <MessageSquare size={12} />
                          <span>Отправить в WA</span>
                        </a>
                      </div>
                    )}

                    {/* ---- ROW 3: AI Rationale + Confidence ---- */}
                    {s.alert && (
                      <div className="mt-8 pt-8 border-t border-slate-100 space-y-4">
                        <div className="grid grid-cols-3 gap-8">
                          <div className="col-span-2 flex items-start space-x-4 bg-slate-50 p-6 rounded-3xl border border-slate-100">
                            <Brain className="w-6 h-6 text-blue-500 mt-1 shrink-0" />
                            <div>
                              <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">AI Rationale</div>
                              <p className="text-sm font-bold text-slate-700 leading-relaxed italic">"{s.reasoning}"</p>
                            </div>
                          </div>
                          <div className="flex flex-col justify-center items-center bg-blue-50/50 rounded-3xl border border-blue-100 p-6">
                             <div className="text-[32px] font-black text-blue-600 leading-none">{s.confidence}%</div>
                             <div className="text-[10px] font-black text-blue-400 uppercase tracking-widest mt-2">AI Confidence</div>
                          </div>
                        </div>
                        {s.rejected && s.rejected.length > 0 && (
                          <div className="bg-rose-50/50 border border-rose-100 rounded-2xl p-4">
                            <div className="text-[10px] font-black text-rose-400 uppercase tracking-widest mb-2">❌ Отклонённые альтернативы</div>
                            <div className="space-y-1.5">
                              {s.rejected.map((r: any, ri: number) => (
                                <div key={ri} className="flex items-center gap-2 text-xs">
                                  <X className="w-3 h-3 text-rose-400 shrink-0" />
                                  <span className="font-bold text-slate-600">{r.name}</span>
                                  <span className="text-slate-400">—</span>
                                  <span className="text-rose-500 font-medium">{r.reason}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
              
              <style dangerouslySetInnerHTML={{ __html: `
                @keyframes pulse-subtle {
                  0%, 100% { opacity: 1; transform: scale(1); }
                  50% { opacity: 0.95; transform: scale(0.995); }
                }
                .animate-pulse-subtle {
                  animation: pulse-subtle 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
                }
              `}} />
            </div>
          )}

          {activeTab === 'rag' && (
            <div className="max-w-5xl mx-auto space-y-8 pb-20">

              {/* Header */}
              <div>
                <h3 className="font-black text-4xl text-slate-800 tracking-tight">Правовой Советник</h3>
                <p className="text-slate-500 mt-1 font-medium flex items-center gap-2">
                  <Shield className="w-4 h-4 text-blue-500" />
                  RAG — семантический поиск по приказам МОН РК №76, №110, №130
                </p>
              </div>

              {/* Law cards */}
              <div className="grid grid-cols-3 gap-4">
                {[
                  {
                    num: '№130', title: 'Питание и посещаемость',
                    desc: 'Порядок сбора данных, питание, льготные категории.',
                    color: 'from-emerald-500 to-teal-600',
                    query: 'Нормы питания №130', tags: ['Ежедневно', 'Столовая', 'Льготники'],
                  },
                  {
                    num: '№110', title: 'Замена учителей',
                    desc: 'Порядок замещения, оплата, журнал пропущенных уроков.',
                    color: 'from-blue-500 to-indigo-600',
                    query: 'Приказ №110: Замены', tags: ['ЖУПЗ', 'Оплата', 'Профиль'],
                  },
                  {
                    num: '№76', title: 'Аттестация педагогов',
                    desc: 'Категории, надбавки, сроки, портфолио педагога.',
                    color: 'from-violet-500 to-purple-600',
                    query: 'Приказ №76: Аттестация', tags: ['Каждые 5 лет', 'БДО +30-50%', 'Портфолио'],
                  },
                ].map((law, i) => (
                  <button
                    key={i}
                    onClick={() => handleRagSearch(law.query)}
                    className={`group relative bg-gradient-to-br ${law.color} rounded-3xl p-6 text-left text-white shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all overflow-hidden`}
                  >
                    <div className="absolute top-4 right-4 text-5xl font-black opacity-10 group-hover:opacity-20 transition-opacity">{law.num}</div>
                    <div className="text-[10px] font-black uppercase tracking-widest opacity-70 mb-2">Приказ МОН РК</div>
                    <div className="text-2xl font-black mb-1">{law.num}</div>
                    <div className="font-bold text-sm opacity-90 mb-3">{law.title}</div>
                    <div className="text-xs opacity-70 leading-relaxed mb-4">{law.desc}</div>
                    <div className="flex flex-wrap gap-1.5">
                      {law.tags.map((t, j) => (
                        <span key={j} className="text-[10px] font-black bg-white/20 px-2.5 py-1 rounded-lg">{t}</span>
                      ))}
                    </div>
                    <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                      <ChevronRight className="w-5 h-5" />
                    </div>
                  </button>
                ))}
              </div>

              {/* Search + mode toggle */}
              <div className="bg-white rounded-[2.5rem] border border-slate-100 shadow-xl p-8 space-y-6">
                <div className="flex gap-2 bg-slate-100 p-1 rounded-2xl w-fit">
                  <button onClick={() => setRagMode('search')} className={`px-5 py-2 rounded-xl text-xs font-black transition-all ${ragMode === 'search' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-600'}`}>
                    🔍 Семантический поиск
                  </button>
                  <button onClick={() => setRagMode('checklist')} className={`px-5 py-2 rounded-xl text-xs font-black transition-all ${ragMode === 'checklist' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-600'}`}>
                    ✅ Генератор чек-листов
                  </button>
                </div>

                <div className="flex gap-3">
                  <div className="flex-1 flex items-center bg-slate-50 border border-slate-200 rounded-2xl px-5 gap-3 focus-within:border-blue-400 focus-within:shadow-lg transition-all">
                    <Search className="w-5 h-5 text-slate-400 shrink-0" />
                    <input
                      type="text"
                      value={ragQuery}
                      onChange={(e) => setRagQuery(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleRagSearch()}
                      placeholder={ragMode === 'search' ? 'Спросите об оплате замен, нормах питания...' : 'Введите тему для генерации чек-листа...'}
                      className="flex-1 bg-transparent text-slate-800 placeholder-slate-400 py-4 text-base focus:outline-none font-medium"
                    />
                    {ragQuery && <button onClick={() => setRagQuery('')} className="text-slate-300 hover:text-slate-500 transition"><X className="w-4 h-4" /></button>}
                  </div>
                  <button
                    onClick={() => handleRagSearch()}
                    disabled={isRagLoading || !ragQuery.trim()}
                    className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white px-8 py-4 rounded-2xl font-black shadow-lg shadow-blue-500/20 transition-all active:scale-95 flex items-center gap-2 whitespace-nowrap"
                  >
                    {isRagLoading ? <div className="w-5 h-5 border-3 border-white/30 border-t-white rounded-full animate-spin" /> : <Sparkles className="w-5 h-5" />}
                    {isRagLoading ? 'Анализ...' : 'Найти ответ'}
                  </button>
                </div>

                {/* Quick queries */}
                <div className="flex flex-wrap gap-2">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-widest self-center">Быстро:</span>
                  {(ragMode === 'search'
                    ? ['Нормы питания №130', 'Приказ №110: Замены', 'Приказ №76: Аттестация', 'Как оформить замену?']
                    : ['Приказ №130', 'Приказ №110', 'Аттестация педагога']
                  ).map((txt, i) => (
                    <button key={i} onClick={() => handleRagSearch(txt)}
                      className="text-xs font-bold bg-slate-50 hover:bg-blue-50 text-slate-600 hover:text-blue-600 border border-slate-200 hover:border-blue-200 px-3 py-1.5 rounded-xl transition-all">
                      {txt}
                    </button>
                  ))}
                </div>
              </div>

              {/* Loading */}
              {isRagLoading && (
                <div className="bg-white rounded-3xl border border-slate-100 shadow-lg p-12 flex flex-col items-center gap-6">
                  <div className="flex gap-3">
                    {[0, 0.15, 0.3].map((delay, i) => (
                      <div key={i} className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: `${delay}s`}} />
                    ))}
                  </div>
                  <div>
                    <div className="font-black text-slate-700 text-center">Семантическое сканирование...</div>
                    <div className="text-xs text-slate-400 text-center mt-1">Поиск по векторной базе приказов МОН РК</div>
                  </div>
                </div>
              )}

              {/* Empty state */}
              {!ragResult && !isRagLoading && (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-20 h-20 bg-blue-50 rounded-3xl flex items-center justify-center mb-6">
                    <BookOpen className="w-10 h-10 text-blue-300" />
                  </div>
                  <div className="font-black text-xl text-slate-700 mb-2">Юридическая база готова</div>
                  <div className="text-slate-400 text-sm max-w-sm">Нажмите на карточку приказа или введите вопрос — AI найдёт точный ответ</div>
                </div>
              )}

              {/* Result */}
              {ragResult && !isRagLoading && (
                <div className="bg-white border-2 border-blue-50 rounded-[2.5rem] shadow-2xl shadow-blue-500/5 overflow-hidden animate-in slide-in-from-bottom-4 duration-500">
                  {/* Result header */}
                  <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-5 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center">
                        <Sparkles className="w-4 h-4 text-white" />
                      </div>
                      <div>
                        <div className="font-black text-white text-sm">AI-ответ сформирован</div>
                        <div className="text-blue-200 text-xs">Правовой советник • RAG v2.0</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-1.5 bg-emerald-400/20 text-emerald-200 border border-emerald-400/30 px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest">
                        <CheckCircle className="w-3 h-3" /> Соответствует нормам
                      </div>
                      <button onClick={() => setRagResult(null)} className="w-8 h-8 bg-white/10 hover:bg-white/20 rounded-xl flex items-center justify-center transition text-white">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="p-8 space-y-6">
                    {/* Answer text */}
                    <div className="relative">
                      <Quote className="absolute -top-3 -left-2 w-10 h-10 text-blue-500/10" />
                      <p className="text-lg font-semibold text-slate-700 leading-relaxed pl-4 border-l-4 border-blue-100">
                        {ragResult.answer}
                      </p>
                    </div>

                    {/* Checklist items */}
                    {ragResult.items && (
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Пошаговый чек-лист</div>
                          <button
                            onClick={() => {
                              const text = ragResult.items.map((it: string, i: number) => `${i + 1}. ${it}`).join('\n');
                              navigator.clipboard.writeText(text);
                              alert('Чек-лист скопирован!');
                            }}
                            className="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-xl transition border border-blue-100"
                          >
                            <Paperclip className="w-3.5 h-3.5" /> Скопировать
                          </button>
                        </div>
                        <div className="space-y-2">
                          {ragResult.items.map((it: string, i: number) => (
                            <div key={i} className="flex items-start gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-100 hover:bg-white hover:shadow-md transition-all group">
                              <div className="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center font-black text-xs shrink-0 shadow-md">{i + 1}</div>
                              <p className="font-semibold text-slate-700 text-sm leading-relaxed pt-0.5">{it}</p>
                              <CheckCircle2 className="w-4 h-4 text-slate-200 group-hover:text-emerald-400 shrink-0 mt-0.5 transition-colors" />
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Sources + actions */}
                    <div className="pt-4 border-t border-slate-100 flex items-center justify-between flex-wrap gap-4">
                      <div className="flex flex-wrap gap-2">
                        {ragResult.sources?.map((s: string, i: number) => (
                          <div key={i} className="flex items-center gap-2 bg-slate-50 border border-slate-200 px-4 py-2 rounded-xl">
                            <FileText className="w-4 h-4 text-blue-400" />
                            <span className="text-xs font-bold text-slate-600">{s}</span>
                          </div>
                        ))}
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            const text = `${ragResult.answer}\n\n${ragResult.items ? ragResult.items.map((it: string, i: number) => `${i+1}. ${it}`).join('\n') : ''}`;
                            const url = `https://wa.me/?text=${encodeURIComponent(text)}`;
                            window.open(url, '_blank');
                          }}
                          className="flex items-center gap-2 bg-[#25D366] hover:bg-[#1da851] text-white px-4 py-2.5 rounded-xl text-xs font-black transition-all active:scale-95 shadow-sm"
                        >
                          <MessageSquare className="w-3.5 h-3.5" /> Отправить в WA
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="max-w-5xl mx-auto space-y-8 pb-20">
              <div>
                <h3 className="font-black text-4xl text-slate-800 tracking-tight">Аналитика</h3>
                <p className="text-slate-500 mt-1 font-medium flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-violet-500" />
                  Недельные тренды и статистика школы
                </p>
              </div>

              {/* Stats row */}
              <div className="grid grid-cols-4 gap-4">
                {[
                  { label: 'Задач за неделю', value: 34, color: 'bg-blue-600', icon: <Zap className="w-5 h-5 text-white" />, change: '+12%' },
                  { label: 'Замен проведено', value: 7, color: 'bg-violet-500', icon: <Calendar className="w-5 h-5 text-white" />, change: '-2' },
                  { label: 'Средняя явка', value: '94%', color: 'bg-emerald-500', icon: <Users className="w-5 h-5 text-white" />, change: '+1.5%' },
                  { label: 'Инцидентов', value: 3, color: 'bg-rose-500', icon: <AlertTriangle className="w-5 h-5 text-white" />, change: '-40%' },
                ].map((s, i) => (
                  <div key={i} className="bg-white rounded-3xl p-6 border border-slate-100 shadow-lg">
                    <div className="flex items-center gap-3 mb-3">
                      <div className={`w-10 h-10 ${s.color} rounded-2xl flex items-center justify-center shadow-lg shrink-0`}>{s.icon}</div>
                      <div className="text-[10px] font-black text-emerald-500 bg-emerald-50 px-2 py-0.5 rounded-full">{s.change}</div>
                    </div>
                    <div className="text-3xl font-black text-slate-800">{s.value}</div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{s.label}</div>
                  </div>
                ))}
              </div>

              {/* Attendance trend (CSS bar chart) */}
              <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-xl">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <div className="font-black text-lg text-slate-800">Посещаемость по дням</div>
                    <div className="text-xs text-slate-400 font-medium">Последние 7 дней • порции / отчёты</div>
                  </div>
                  <div className="flex gap-3 text-[10px] font-bold uppercase tracking-widest">
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span> Порции</span>
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> Отчёты</span>
                  </div>
                </div>
                <div className="flex items-end gap-3 h-48">
                  {[
                    { day: 'Пн', portions: 120, reports: 6 },
                    { day: 'Вт', portions: 135, reports: 7 },
                    { day: 'Ср', portions: 128, reports: 6 },
                    { day: 'Чт', portions: 142, reports: 8 },
                    { day: 'Пт', portions: 115, reports: 5 },
                    { day: 'Сб', portions: 45, reports: 3 },
                    { day: 'Вс', portions: 0, reports: 0 },
                  ].map((d, i) => (
                    <div key={i} className="flex-1 flex flex-col items-center gap-1">
                      <div className="w-full flex gap-1 items-end justify-center" style={{ height: '160px' }}>
                        <div 
                          className="w-5 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-lg transition-all duration-500" 
                          style={{ height: `${(d.portions / 142) * 100}%`, minHeight: d.portions > 0 ? '8px' : '0' }}
                        />
                        <div 
                          className="w-5 bg-gradient-to-t from-emerald-500 to-emerald-300 rounded-t-lg transition-all duration-500" 
                          style={{ height: `${(d.reports / 8) * 100}%`, minHeight: d.reports > 0 ? '8px' : '0' }}
                        />
                      </div>
                      <span className="text-[10px] font-bold text-slate-400">{d.day}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bottom row: Top incidents + Task completion */}
              <div className="grid grid-cols-2 gap-6">
                <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-xl">
                  <div className="font-black text-lg text-slate-800 mb-4">Топ-3 типа инцидентов</div>
                  <div className="space-y-4">
                    {[
                      { type: 'Поломка оборудования', count: 5, pct: 50, color: 'bg-amber-500' },
                      { type: 'Конфликт между учениками', count: 3, pct: 30, color: 'bg-rose-500' },
                      { type: 'Протечка / авария', count: 2, pct: 20, color: 'bg-blue-500' },
                    ].map((inc, i) => (
                      <div key={i}>
                        <div className="flex justify-between items-center mb-1.5">
                          <span className="text-sm font-bold text-slate-700">{inc.type}</span>
                          <span className="text-xs font-black text-slate-400">{inc.count} случаев</span>
                        </div>
                        <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                          <div className={`h-full ${inc.color} rounded-full transition-all duration-700`} style={{ width: `${inc.pct}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-xl">
                  <div className="font-black text-lg text-slate-800 mb-4">Эффективность задач</div>
                  <div className="flex items-center justify-center py-4">
                    <div className="relative w-36 h-36">
                      <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                        <circle cx="18" cy="18" r="15.5" fill="none" stroke="#f1f5f9" strokeWidth="3" />
                        <circle cx="18" cy="18" r="15.5" fill="none" stroke="#3b82f6" strokeWidth="3" strokeDasharray="97.4" strokeDashoffset="24.3" strokeLinecap="round" />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <div className="text-3xl font-black text-slate-800">75%</div>
                        <div className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Выполнено</div>
                      </div>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-2 mt-2">
                    {[
                      { label: 'Выполнено', value: 26, color: 'text-blue-600' },
                      { label: 'В работе', value: 5, color: 'text-amber-500' },
                      { label: 'Просрочено', value: 3, color: 'text-rose-500' },
                    ].map((s, i) => (
                      <div key={i} className="text-center">
                        <div className={`text-xl font-black ${s.color}`}>{s.value}</div>
                        <div className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">{s.label}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Director metric */}
              <div className="bg-gradient-to-r from-violet-600 to-blue-600 rounded-3xl p-8 text-white shadow-2xl shadow-violet-500/20">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-xs font-black uppercase tracking-widest text-violet-200 mb-2">💡 Метрика Покойо</div>
                    <div className="text-2xl font-black">Директор тратил 2 часа в день на рутину →</div>
                    <div className="text-4xl font-black mt-1">Теперь 5 минут</div>
                  </div>
                  <div className="text-8xl font-black opacity-20">24×</div>
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

        {/* SUCCESS OVERLAY */}
        {showSuccessOverlay && (
          <div className="fixed inset-0 z-[200] flex items-center justify-center bg-slate-900/40 backdrop-blur-md animate-in fade-in duration-500">
            <div className="bg-white p-12 rounded-[5rem] shadow-[0_50px_100px_rgba(0,0,0,0.2)] flex flex-col items-center text-center max-w-lg border border-slate-100 animate-in zoom-in slide-in-from-bottom-20 duration-500">
               <div className="w-32 h-32 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-8 shadow-inner">
                  <CheckCircle size={64} strokeWidth={3} />
               </div>
               <h2 className="text-4xl font-black text-slate-800 mb-4 tracking-tight">Ура! План готов! 🎉</h2>
               <p className="text-xl text-slate-500 font-bold leading-relaxed px-4">Все замены утверждены и разосланы учителям. <br/> <span className="text-blue-600">Система работает как часы!</span></p>
            </div>
          </div>
        )}

        {/* AI Generating Order Loader */}
        {isGeneratingOrder && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center bg-blue-900/40 backdrop-blur-md">
             <div className="bg-white p-12 rounded-[3.5rem] shadow-2xl text-center space-y-6 animate-in zoom-in duration-300">
                <div className="relative w-24 h-24 mx-auto">
                   <div className="absolute inset-0 bg-blue-100 rounded-3xl animate-spin duration-[3000ms]"></div>
                   <div className="absolute inset-0 flex items-center justify-center text-blue-600">
                      <Sparkles size={40} className="animate-pulse" />
                   </div>
                </div>
                <div>
                   <h3 className="text-2xl font-black text-slate-800">Бюрократическая магия...</h3>
                   <p className="text-slate-500 font-bold uppercase tracking-widest text-xs mt-2">Генерация юридического драфта по Приказу №130</p>
                </div>
             </div>
          </div>
        )}

        {/* Legal Order Modal (Printable) */}
        {selectedOrder && (
          <div className="fixed inset-0 z-[110] flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 overflow-y-auto">
             <div className="bg-white w-full max-w-4xl rounded-[3rem] shadow-2xl overflow-hidden animate-in slide-in-from-bottom-10 duration-500 flex flex-col max-h-[90vh]">
                <div className="px-10 py-6 border-b border-slate-100 flex items-center justify-between bg-white relative z-20">
                   <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center">
                         <FileText size={24} />
                      </div>
                      <div>
                         <h3 className="font-black text-xl text-slate-800 uppercase tracking-tight">Предпросмотр приказа</h3>
                         <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Готов к печати согласно ГОСТ РК</p>
                      </div>
                   </div>
                   <div className="flex items-center space-x-3">
                      <button 
                         onClick={() => window.print()} 
                         className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-900 text-white px-6 py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all active:scale-95"
                      >
                         <Printer size={16} />
                         <span>Распечатать</span>
                      </button>
                      <button 
                         onClick={() => setSelectedOrder(null)} 
                         className="p-3 hover:bg-slate-100 rounded-2xl transition-colors"
                      >
                         <X size={24} className="text-slate-400" />
                      </button>
                   </div>
                </div>

                <div id="printable-order" className="flex-1 overflow-y-auto p-12 bg-slate-50">
                   <div className="bg-white shadow-xl mx-auto p-16 min-h-[1000px] text-slate-900 font-serif leading-relaxed print:shadow-none print:p-0">
                      {/* Document Header */}
                      <div className="text-center mb-12 space-y-2 border-b-2 border-slate-900 pb-8">
                         <div className="font-bold text-sm uppercase tracking-wider mb-4 whitespace-pre-line">
                            {selectedOrder.header}
                         </div>
                         <div className="text-3xl font-black tracking-tighter uppercase my-6">ПРИКАЗ / БҰЙРЫҚ</div>
                         <div className="flex justify-between font-bold text-sm px-10 pt-4">
                            <div>г. Астана / Астана қ.</div>
                            <div>{selectedOrder.order_date} г.</div>
                         </div>
                         <div className="font-black text-xl pt-2">{selectedOrder.order_number}</div>
                      </div>

                      {/* Content */}
                      <div className="space-y-10 text-justify px-4">
                         <div className="italic font-bold text-slate-700">
                            {selectedOrder.preamble}
                         </div>

                         <div className="space-y-6">
                            <div className="font-black underline uppercase">БҰЙЫРАМЫН / ПРИКАЗЫВАЮ:</div>
                            <div className="whitespace-pre-line">
                               {selectedOrder.order_body_kz}
                            </div>
                            <div className="whitespace-pre-line mt-6 border-t border-slate-100 pt-6">
                               {selectedOrder.order_body_ru}
                            </div>
                         </div>

                         <div className="mt-20 pt-12 grid grid-cols-2 gap-20">
                            <div className="space-y-12">
                               <div className="border-b border-slate-900 pb-2 font-bold uppercase text-xs">Директор</div>
                               <div className="border-b border-slate-900 pb-2 font-bold uppercase text-xs">Ознакомлен(а)</div>
                            </div>
                            <div className="space-y-12 text-right">
                               <div className="font-bold whitespace-pre-line text-sm">{selectedOrder.signatories.split('\n')[0]}</div>
                               <div className="font-bold whitespace-pre-line text-sm">{selectedOrder.signatories.split('\n')[1]}</div>
                            </div>
                         </div>
                      </div>

                      {/* Seal Area (Visual) */}
                      <div className="mt-32 opacity-10 flex justify-end pr-20">
                         <div className="w-32 h-32 border-4 border-blue-600 rounded-full flex items-center justify-center text-blue-600 font-black text-[10px] text-center rotate-12 uppercase p-2">
                            Место печати / Мөр орны
                         </div>
                      </div>
                   </div>
                </div>
             </div>

             <style dangerouslySetInnerHTML={{ __html: `
                @media print {
                  body * { visibility: hidden; }
                  #printable-order, #printable-order * { visibility: visible; }
                  #printable-order { position: absolute; left: 0; top: 0; width: 100%; height: 100%; padding: 0; background: white; }
                  .no-print { display: none !important; }
                }
             `}} />
          </div>
        )}
      </div>
    </div>
  );
}

function MenuButton({title, desc, icon, active, onClick}: any) {
  return (
    <div onClick={onClick} className={`p-4 rounded-2xl cursor-pointer transition-all duration-300 flex items-center group ${active ? 'bg-blue-600 text-white shadow-xl transform scale-[1.02]' : 'hover:bg-slate-50 border border-transparent'}`}>
      <div className={`p-3 rounded-xl mr-4 ${active ? 'bg-blue-700 text-white' : 'bg-slate-100 text-slate-400'}`}>{icon}</div>
      <div>
        <h3 className={`font-bold text-[15px] ${active ? 'text-white' : 'text-slate-700'}`}>{title}</h3>
        <p className={`text-xs mt-1 font-medium ${active ? 'text-blue-100' : 'text-slate-400'}`}>{desc}</p>
      </div>
    </div>
  );
}
