import React from 'react';
import { Modal, Divider } from 'antd';

const ModalComponents = (props: any) => {
  const { visible, setVisible, indicatorDetail } = props;

  return (
    <Modal
      title="指标解释"
      centered
      visible={visible}
      onOk={() => setVisible(false)}
      onCancel={() => setVisible(false)}
      // width={800}
      footer={null}
    >
      <div style={{ display: 'flex', height: '300px' }}>
        <div className="left" style={{ flex: 1 }}>
          <b>{indicatorDetail?.indicator}</b>
          <div style={{ height: '265px', overflow: 'auto', marginTop: '12px' }}>
            {indicatorDetail?.description}
          </div>
        </div>
        {indicatorDetail?.destinationTranslation && (
          <>
            <Divider style={{ height: '305px' }} type="vertical" />
            <div className="right" style={{ flex: 1 }}>
              <b>{indicatorDetail?.indicatorTransaction}</b>
              <div style={{ height: '265px', overflow: 'auto', marginTop: '12px' }}>
                {indicatorDetail?.destinationTranslation}
              </div>
            </div>
          </>
        )}
      </div>
    </Modal>
  );
};

export default ModalComponents;
