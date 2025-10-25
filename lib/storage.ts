// ハイブリッドストレージ管理（ローカルストレージ + Firestore）
import { User, Record, Session, ModeType } from './types';

// Firestoreを使用するかどうかのフラグ
const USE_FIRESTORE = typeof window !== 'undefined' && 
  process.env.NEXT_PUBLIC_FIREBASE_API_KEY !== undefined &&
  process.env.NEXT_PUBLIC_FIREBASE_API_KEY !== '';

// Firestoreモジュール（動的インポート）
let firestoreModule: typeof import('./firestore') | null = null;

// Firestoreモジュールの遅延ロード
const loadFirestore = async () => {
  if (!firestoreModule && USE_FIRESTORE) {
    try {
      firestoreModule = await import('./firestore');
    } catch (error) {
      console.error('Failed to load Firestore module:', error);
    }
  }
  return firestoreModule;
};

const STORAGE_KEYS = {
  USER: 'reaction-app-user',
  RECORDS: 'reaction-app-records',
  SESSION: 'reaction-app-session',
} as const;

// ローカルのユーザーIDを取得
const getLocalUserId = (): string | null => {
  if (typeof window === 'undefined') return null;
  const data = localStorage.getItem(STORAGE_KEYS.USER);
  if (!data) return null;
  try {
    const user = JSON.parse(data);
    return user.id;
  } catch {
    return null;
  }
};

// ユーザー管理
export const getUser = async (): Promise<User | null> => {
  // ローカルストレージから取得
  if (typeof window === 'undefined') return null;
  const data = localStorage.getItem(STORAGE_KEYS.USER);
  if (!data) return null;
  
  try {
    const localUser = JSON.parse(data);
    
    // Firestoreが有効な場合、Firestoreからも取得して同期
    if (USE_FIRESTORE) {
      const firestore = await loadFirestore();
      if (firestore) {
        try {
          const firestoreUser = await firestore.getUser(localUser.id);
          if (firestoreUser) {
            return firestoreUser;
          }
        } catch (error) {
          console.error('Firestore getUser error:', error);
        }
      }
    }
    
    return localUser;
  } catch {
    return null;
  }
};

export const saveUser = async (user: User): Promise<void> => {
  // ローカルストレージに保存
  if (typeof window !== 'undefined') {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
  }
  
  // Firestoreに保存
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        await firestore.saveUser(user);
      } catch (error) {
        console.error('Firestore saveUser error:', error);
      }
    }
  }
};

export const clearUser = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(STORAGE_KEYS.USER);
};

// 記録管理
export const getRecords = async (): Promise<Record[]> => {
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        return await firestore.getRecords();
      } catch (error) {
        console.error('Firestore getRecords error:', error);
      }
    }
  }
  
  // フォールバック: ローカルストレージ
  if (typeof window === 'undefined') return [];
  const data = localStorage.getItem(STORAGE_KEYS.RECORDS);
  try {
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
};

export const addRecord = async (record: Omit<Record, 'id' | 'createdAt'>): Promise<Record> => {
  const newRecord: Record = {
    ...record,
    id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    createdAt: new Date().toISOString(),
  };
  
  // Firestoreに保存
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        return await firestore.addRecord(record);
      } catch (error) {
        console.error('Firestore addRecord error:', error);
      }
    }
  }
  
  // フォールバック: ローカルストレージ
  const records = await getRecords();
  records.push(newRecord);
  
  if (typeof window !== 'undefined') {
    localStorage.setItem(STORAGE_KEYS.RECORDS, JSON.stringify(records));
  }
  
  return newRecord;
};

export const getRecordsByUser = async (userId: string): Promise<Record[]> => {
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        return await firestore.getRecordsByUser(userId);
      } catch (error) {
        console.error('Firestore getRecordsByUser error:', error);
      }
    }
  }
  
  const records = await getRecords();
  return records.filter(r => r.userId === userId);
};

export const getRecordsByMode = async (mode: string): Promise<Record[]> => {
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        return await firestore.getRecordsByMode(mode);
      } catch (error) {
        console.error('Firestore getRecordsByMode error:', error);
      }
    }
  }
  
  const records = await getRecords();
  return records.filter(r => r.mode === mode);
};

export const getRecordsByModeType = async (mode: ModeType): Promise<Record[]> => {
  return getRecordsByMode(mode);
};

// セッション管理
export const getCurrentSession = async (): Promise<Session> => {
  const defaultSession: Session = {
    id: 'ota-city-2025',
    name: '島根県大田市 × 日本体育大学 特別講座',
    date: new Date().toISOString().split('T')[0],
  };
  
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        return await firestore.getCurrentSession();
      } catch (error) {
        console.error('Firestore getCurrentSession error:', error);
      }
    }
  }
  
  // フォールバック: ローカルストレージ
  if (typeof window === 'undefined') {
    return defaultSession;
  }
  
  const data = localStorage.getItem(STORAGE_KEYS.SESSION);
  if (data) {
    try {
      return JSON.parse(data);
    } catch {
      return defaultSession;
    }
  }
  
  localStorage.setItem(STORAGE_KEYS.SESSION, JSON.stringify(defaultSession));
  return defaultSession;
};

export const setSession = async (session: Session): Promise<void> => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(STORAGE_KEYS.SESSION, JSON.stringify(session));
  }
  
  if (USE_FIRESTORE) {
    const firestore = await loadFirestore();
    if (firestore) {
      try {
        await firestore.setSession(session);
      } catch (error) {
        console.error('Firestore setSession error:', error);
      }
    }
  }
};
