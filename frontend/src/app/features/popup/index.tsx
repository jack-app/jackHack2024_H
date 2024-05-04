import { useState } from 'react';
import { Settings } from '../settings';
import { TaskList } from '../taskList';

export const PopUp = () => {
  type ShowTabType = 'taskList' | 'settings';

  const [showTab, setShowTab] = useState<ShowTabType>('taskList');
  return (
    <div className="w-96">
      <h2>
        <span className=" cursor-pointer" onClick={() => setShowTab('taskList')}>
          課題一覧
        </span>
        <span> | </span>
        <span className=" cursor-pointer" onClick={() => setShowTab('settings')}>
          設定
        </span>
      </h2>
      {showTab === 'taskList' && <TaskList />}
      {showTab === 'settings' && <Settings />}
      <a href="#" id="page_top" className="page_top_btn"></a>
    </div>
  );
};
