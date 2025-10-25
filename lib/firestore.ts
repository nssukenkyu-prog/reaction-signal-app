// Firestore データ管理
import { 
  collection, 
  doc, 
  getDoc, 
  getDocs, 
  setDoc, 
  query, 
  where, 
  orderBy,
} from 'firebase/firestore';
import { db } from './firebase';
import { User, Record, Session, ModeType } from './types';

// コレクション名
const COLLECTIONS = {
  USERS: 'users',
  RECORDS: 'records',
  SESSIONS: 'sessions',
} as const;

// ユーザー管理
export const getUser = async (userId: string): Promise<User | null> => {
  try {
    const userDoc = await getDoc(doc(db, COLLECTIONS.USERS, userId));
    if (userDoc.exists()) {
      return userDoc.data() as User;
    }
    return null;
  } catch (error) {
    console.error('Error getting user:', error);
    return null;
  }
};

export const saveUser = async (user: User): Promise<void> => {
  try {
    await setDoc(doc(db, COLLECTIONS.USERS, user.id), user);
  } catch (error) {
    console.error('Error saving user:', error);
    throw error;
  }
};

// 記録管理
export const getRecords = async (): Promise<Record[]> => {
  try {
    const recordsSnapshot = await getDocs(collection(db, COLLECTIONS.RECORDS));
    return recordsSnapshot.docs.map(doc => doc.data() as Record);
  } catch (error) {
    console.error('Error getting records:', error);
    return [];
  }
};

export const addRecord = async (record: Omit<Record, 'id' | 'createdAt'>): Promise<Record> => {
  try {
    const newRecord: Record = {
      ...record,
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      createdAt: new Date().toISOString(),
    };
    
    await setDoc(doc(db, COLLECTIONS.RECORDS, newRecord.id), newRecord);
    return newRecord;
  } catch (error) {
    console.error('Error adding record:', error);
    throw error;
  }
};

export const getRecordsByUser = async (userId: string): Promise<Record[]> => {
  try {
    const q = query(
      collection(db, COLLECTIONS.RECORDS),
      where('userId', '==', userId)
    );
    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map(doc => doc.data() as Record);
  } catch (error) {
    console.error('Error getting user records:', error);
    return [];
  }
};

export const getRecordsByMode = async (mode: string): Promise<Record[]> => {
  try {
    const q = query(
      collection(db, COLLECTIONS.RECORDS),
      where('mode', '==', mode),
      orderBy('reactionTime', 'asc')
    );
    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map(doc => doc.data() as Record);
  } catch (error) {
    console.error('Error getting mode records:', error);
    return [];
  }
};

export const getRecordsByModeType = async (mode: ModeType): Promise<Record[]> => {
  return getRecordsByMode(mode);
};

// セッション管理
export const getCurrentSession = async (): Promise<Session> => {
  const defaultSession: Session = {
    id: 'default-session',
    name: '島根県大田市 × 日本体育大学 特別講座',
    date: new Date().toISOString().split('T')[0],
  };

  try {
    const sessionDoc = await getDoc(doc(db, COLLECTIONS.SESSIONS, 'default-session'));
    if (sessionDoc.exists()) {
      return sessionDoc.data() as Session;
    }
    
    await setDoc(doc(db, COLLECTIONS.SESSIONS, 'default-session'), defaultSession);
    return defaultSession;
  } catch (error) {
    console.error('Error getting session:', error);
    return defaultSession;
  }
};

export const setSession = async (session: Session): Promise<void> => {
  try {
    await setDoc(doc(db, COLLECTIONS.SESSIONS, session.id), session);
  } catch (error) {
    console.error('Error setting session:', error);
    throw error;
  }
};
